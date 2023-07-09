from hamcrest import assert_that, has_properties

from dm_api_account.models.user_envelope_model import UserRole, Rating
from services.dm_api_account import Facade


def test_delete_v1_account_login_all():
    api = Facade(host="http://localhost:5051")

    login = "login120"
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
    api.login.set_headers(headers=token)
    api.login.logout_user_from_all_devices()
