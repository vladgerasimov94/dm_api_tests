from datetime import datetime

import structlog

from dm_api_account.models.reset_password_model import ResetPassword
from dm_api_account.models.user_envelope_model import UserRole
from services.dm_api_account import DmApiAccount
from hamcrest import assert_that, instance_of, has_properties

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)
    ]
)


def test_post_v1_account_password():
    api = DmApiAccount(host="http://localhost:5051")
    login = "login94"
    json = ResetPassword(
        login=login,
        email=f"{login}@mail.ru"
    )
    response = api.account.post_v1_account_password(json=json)

    assert_that(response.resource, has_properties(
        {
            "login": login,
            "roles": [UserRole.GUEST, UserRole.PLAYER],
            "registration": instance_of(datetime)
        }
    ))
