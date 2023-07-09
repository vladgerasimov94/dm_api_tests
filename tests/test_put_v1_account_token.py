from services.dm_api_account import Facade
import structlog
from dm_api_account.models.user_envelope_model import UserRole, Rating
from hamcrest import assert_that, has_properties

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)
    ]
)


def test_put_v1_account_token():
    api = Facade(host="http://localhost:5051")

    login = "login123"
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
