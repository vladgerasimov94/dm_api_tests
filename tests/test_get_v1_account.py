from datetime import datetime

from hamcrest import assert_that, has_properties, instance_of

from dm_api_account.models.user_details_envelope_model import UserRole
from services.dm_api_account import DmApiAccount


def test_get_v1_account():
    api = DmApiAccount(host="http://localhost:5051")
    response = api.account.get_v1_account()
    assert_that(response.resource, has_properties(
        {
            "login": "login95",
            "roles": [UserRole.GUEST, UserRole.PLAYER],
            "registration": instance_of(datetime)
        }
    ))
