import structlog

from dm_api_account.models.user_envelope_model import UserRole, Rating
from services.dm_api_account import Facade
from hamcrest import assert_that, has_properties

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)
    ]
)


def test_put_v1_account_password():
    api = Facade(host="http://localhost:5051")

    login = "login122"
    email = f"{login}@mail.ru"
    password = login + login

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

    token = api.login.get_auth_token(login=login, password=password)
    api.account.set_headers(headers=token)

    api.account.reset_registered_user_password(login=login, email=email)

    response = api.account.change_registered_user_password(
        login=login,
        old_password=password,
        new_password=f"new_{password}"
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
