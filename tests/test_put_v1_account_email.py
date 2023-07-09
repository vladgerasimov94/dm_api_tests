from dm_api_account.models.user_envelope_model import UserRole, Rating
from services.dm_api_account import Facade
from hamcrest import assert_that, has_properties

import structlog

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)
    ]
)


def test_put_v1_account_email():
    api = Facade(host="http://localhost:5051")
    login = "login121"
    password = login + login
    email = f"{login}@mail.ru"
    api.account.register_new_user(
        login=login,
        email=email,
        password=password
    )

    response = api.account.activate_registered_user(login=login)
    assert_that(response.resource, has_properties(
        {
            "login": login,
            "roles": [UserRole.GUEST, UserRole.PLAYER],
            "rating": Rating(
                enabled=True,
                quality=0,
                quantity=0
            )
        }
    ))

    response = api.account.change_registered_user_email(
        login=login,
        password=password,
        email=f"new_{email}"
    )
    assert_that(response.resource, has_properties(
        {
            "login": login,
            "roles": [UserRole.GUEST, UserRole.PLAYER],
            "rating": Rating(
                enabled=True,
                quality=0,
                quantity=0
            )
        }
    ))
