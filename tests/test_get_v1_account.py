from datetime import datetime

import structlog
from hamcrest import assert_that, has_properties, instance_of

from dm_api_account.models.user_details_envelope_model import UserRole
from services.dm_api_account import Facade

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)
    ]
)


def test_get_v1_account():
    api = Facade(host="http://localhost:5051")

    login = "login119"
    email = f"{login}@mail.ru"
    password = login + login

    api.account.register_new_user(
        login=login,
        email=email,
        password=password
    )
    api.account.activate_registered_user(login=login)
    token = api.login.get_auth_token(login=login, password=password)
    api.account.set_headers(headers=token)

    response = api.account.get_current_user_info()
    assert_that(response.resource, has_properties(
        {
            "login": login,
            "roles": [UserRole.GUEST, UserRole.PLAYER],
            "registration": instance_of(datetime)
        }
    ))
