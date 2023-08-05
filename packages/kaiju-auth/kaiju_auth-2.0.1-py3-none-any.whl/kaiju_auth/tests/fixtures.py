"""
Place your pytest fixtures here.
"""

import pytest

from kaiju_db.tests.fixtures import *
from kaiju_tools.rpc.tests.fixtures import *
from kaiju_tools.rpc import AbstractRPCCompatible

from ..services import *


@pytest.fixture
def permission():
    _row = {
        'id': AbstractRPCCompatible.PermissionKeys.GLOBAL_USER_PERMISSION,
        'enabled': True,
        'tag': 'user',
        'description': 'some kind of user permission'
    }
    return _row


@pytest.fixture
def group():
    _row = {
        'id': 'group',
        'tag': 'user',
        'description': 'some group'
    }
    return _row


@pytest.fixture
def user():
    _row = {
        'username': 'shitman',
        'email': 'sample@mail.ru',
        'password': '_password5394593_'
    }
    return _row
