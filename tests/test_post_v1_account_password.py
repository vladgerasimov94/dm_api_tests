from datetime import datetime

import structlog

from dm_api_account.models.user_envelope_model import UserRole
from services.dm_api_account import Facade
from hamcrest import assert_that, instance_of, has_properties

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)
    ]
)


def test_post_v1_account_password():
    api = Facade(host="http://localhost:5051")

    login = "login120"
    email = f"{login}@mail.ru"
    response = api.account.reset_registered_user_password(login=login, email=email)
    assert_that(response.resource, has_properties(
        {
            "login": login,
            "roles": [UserRole.GUEST, UserRole.PLAYER],
            "registration": instance_of(datetime)
        }
    ))
