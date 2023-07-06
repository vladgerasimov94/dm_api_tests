from datetime import datetime

import structlog

from dm_api_account.models.reset_password_model import ResetPassword
from dm_api_account.models.user_envelope_model import UserRole
from services.dm_api_account import DmApiAccount
from hamcrest import assert_that, equal_to, contains_exactly, has_key, instance_of

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)
    ]
)


def test_post_v1_account_password():
    api = DmApiAccount(host="http://localhost:5051")
    login = "login76"
    json = ResetPassword(
        login=login,
        email=f"{login}@mail.ru"
    )
    response = api.account.post_v1_account_password(json=json)

    assert_that(response.metadata, has_key("email"))
    assert_that(response.resource.login, equal_to(login))
    assert_that(response.resource.registration, instance_of(datetime))
    assert_that(response.resource.roles, contains_exactly(UserRole.GUEST, UserRole.PLAYER))
