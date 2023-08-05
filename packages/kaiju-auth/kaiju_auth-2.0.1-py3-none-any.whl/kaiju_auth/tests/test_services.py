import pytest
from aiohttp_session import SESSION_KEY
from aiohttp.test_utils import make_mocked_request

from kaiju_tools.exceptions import NotFound, Conflict, NotAuthorized, ValidationError
from kaiju_tools.cache.services import LocalCacheService

from .fixtures import *
from ..services import *


@pytest.mark.asyncio
async def test_permission_service(database, database_service, permission, logger):
    service = PermissionService(app=None, database_service=database_service, logger=logger)

    async with database_service:

        await service.init()

        logger.debug('Testing inserts')
        result = await service.create(permission, columns=['id'])
        assert result['id'] == permission['id']

        with pytest.raises(Conflict):
            await service.create(permission)

        logger.debug('Testing selection / filtering')
        result = await service.get_all_permissions(group_by_tag=True)
        assert result[0]['tag'] == permission['tag']
        assert len(result[0]['permissions']) == 1


@pytest.mark.asyncio
async def test_group_service(database, database_service, permission, group, logger):
    permission_service = PermissionService(app=None, database_service=database_service, logger=logger)
    group_service = GroupService(
        app=None, database_service=database_service, permission_service=permission_service, logger=logger
    )

    async with database_service:

        await permission_service.init()
        await group_service.init()

        permission1 = {**permission}
        permission2 = {**permission}
        permission2['id'] = 'other_permission'
        permission3 = {**permission}
        permission3['id'] = 'inactive_permission'
        permission3['enabled'] = False

        logger.debug('Checking adding permissions')
        await permission_service.create([permission1, permission2, permission3])
        await group_service.create(group)

        permissions = await group_service.get_permissions(group['id'])
        assert len(permissions) == 0

        logger.debug('Checking modification')
        new_permissions = {permission1['id']: True, permission2['id']: True, permission3['id']: True, 'unknown': True}
        permissions = await group_service.modify_permissions(group['id'], new_permissions)
        assert permission1['id'] in permissions
        assert permission3['id'] not in permissions
        assert 'unknown' not in permissions

        new_permissions[permission1['id']] = False
        permissions = await group_service.modify_permissions(group['id'], new_permissions)
        assert permission1['id'] not in permissions

        logger.debug('Checking various strange data input')
        await group_service.modify_permissions(group['id'], {})
        await group_service.get_permissions([])


@pytest.mark.asyncio
async def test_user_service(database, database_service, permission, group, user, logger):
    group_id, permission_id = group['id'], permission['id']
    username, password = user['username'], user['password']
    permission_service = PermissionService(app=None, database_service=database_service, logger=logger)
    group_service = GroupService(
        app=None, database_service=database_service, permission_service=permission_service, logger=logger
    )
    user_service = UserService(
        app=None, database_service=database_service, group_service=group_service, default_group=group_id, logger=logger
    )

    async with database_service:

        await permission_service.init()
        await group_service.init()
        await user_service.init()

        await permission_service.create(permission)
        await group_service.create(group)
        await group_service.modify_permissions(group_id, {permission_id: True})

        logger.info('Registration and auth')
        data = await user_service.register(**user)
        user_id = data['id']
        assert permission_id in data['permissions']
        data = await user_service.auth(username, password)
        assert data['id'] == user_id
        data = await user_service.get(user_id, columns='*')
        assert 'password' not in data

        with pytest.raises(Conflict):
            await user_service.register(**user)

        logger.info('Changing groups')
        await user_service.modify_user_groups(user_id, {group_id: False})
        permissions = await user_service.get_user_permissions(user_id)
        assert permission_id not in permissions

        logger.info('Changing password')
        new_password = '_6456456new_password5345_'

        with pytest.raises(NotAuthorized):
            await user_service.change_password(username, 'worng', new_password=new_password)

        with pytest.raises(ValidationError):
            await user_service.change_password(username, password, new_password='qwerty')

        await user_service.change_password(username, password, new_password=new_password)
        password = new_password
        await user_service.auth(username, password)


@pytest.mark.asyncio
async def test_http_login_service(database, database_service, permission, group, user, logger):
    group_id, permission_id = group['id'], permission['id']
    permission_service = PermissionService(app=None, database_service=database_service, logger=logger)
    group_service = GroupService(
        app=None, database_service=database_service, permission_service=permission_service, logger=logger
    )
    user_service = UserService(
        app=None,
        database_service=database_service,
        default_group=group_id,
        default_nonlogin_group=None,
        group_service=group_service,
        logger=logger,
    )
    cache = LocalCacheService(app=None, logger=logger)
    session_service = SessionService(app=None, database_service=database_service, cache_service=cache, logger=logger)
    http_session_service = HTTPSessionService(app=None, session_service=session_service, logger=logger)
    keystore_service = KeystoreService(app=None, cache_service=cache, logger=logger)
    keystore_service._daemon_sleep_interval = 0.1
    token_service = JWTService(app=None, keystore=keystore_service, logger=logger)
    login_service = HTTPLoginService(
        app=None,
        user_service=user_service,
        session_service=http_session_service,
        token_service=token_service,
        logger=logger,
    )

    async with database_service:

        for service in (
            permission_service,
            group_service,
            user_service,
            session_service,
            http_session_service,
            keystore_service,
            token_service,
            login_service,
        ):
            await service.init()

        await permission_service.create(permission)
        await group_service.create(group)
        await group_service.modify_permissions(group_id, {permission_id: True})

        logger.info('Testing registration')
        request = make_mocked_request(method='POST', path='/rpc')
        await login_service.register(request, **user)
        users = await user_service.list()
        user_id = users['data'][0]['id']
        session = request[SESSION_KEY]
        assert permission_id in session['permissions']

        logger.info('Testing logout')
        await login_service.logout(request)
        assert SESSION_KEY not in request

        logger.info('Testing login')
        request = make_mocked_request(method='POST', path='/rpc')
        await login_service.login(request, username=user['username'], password=user['password'])
        session = request[SESSION_KEY]
        assert session['user_id'] == users['data'][0]['id']

        logger.info('Testing user settings')
        await user_service.update_profile(session, {'language': 'ru'})
        data = await user_service.get_profile(session)
        assert data['id'] == session['user_id'] == user_id
        assert data['settings']['language'] == 'ru'

        logger.info('Testing tokens')
        tokens = await login_service.jwt_get(username=user['username'], password=user['password'])
        tokens = await login_service.jwt_refresh(refresh=tokens['refresh'])
        logger.debug(tokens)

        jwt_client_service = JWTClientService(
            app=None,
            auth={'username': user['username'], 'password': user['password']},
            login_service=login_service,
            logger=logger,
        )
        async with jwt_client_service:
            # testing token event locks
            await asyncio.gather(jwt_client_service.get_token(), jwt_client_service.get_token())

        logger.info('Testing specific tokens by user id')
        tokens = await login_service.jwt_get_by_user_id(session['user_id'], ttl=10000)
        logger.debug(tokens)


@pytest.mark.asyncio
async def test_keystore_service(logger):
    cache = LocalCacheService(app=None, logger=logger)
    service_1 = KeystoreService(app=None, cache_service=cache, logger=logger)
    service_2 = KeystoreService(app=None, cache_service=cache, logger=logger)
    service_1._daemon_sleep_interval = 0.1
    service_2._daemon_sleep_interval = 0.1
    async with service_1:
        async with service_2:
            kid, _ = await service_1.get_encryption_key()
            pkey_1 = await service_1.get_public_key()
            pkey_2 = await service_2.get_public_key(kid)
            assert pkey_1.export_public() == pkey_2.export_public()


@pytest.mark.asyncio
async def test_token_service(logger):
    cache = LocalCacheService(app=None, logger=logger)
    keystore = KeystoreService(app=None, cache_service=cache, logger=logger)
    tokens = JWTService(app=None, keystore=keystore, logger=logger)
    async with keystore:
        async with tokens:
            logger.info('Checking basic workflow')
            access, refresh = await tokens.generate_token_pair()
            await tokens.verify_token(access)
            access, refresh = await tokens.refresh_token(refresh)
            await tokens.verify_token(access.serialize(compact=True))

            logger.info('Testing invalid token formats.')
            with pytest.raises(NotAuthorized):
                await tokens.verify_token('shit')
