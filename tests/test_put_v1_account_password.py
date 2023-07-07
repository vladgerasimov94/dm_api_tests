from dm_api_account.models.change_password_model import ChangePassword
from dm_api_account.models.registration_model import Registration
from dm_api_account.models.user_envelope_model import UserRole, Rating
from services.dm_api_account import DmApiAccount
from services.mailhog import MailhogApi
from hamcrest import assert_that, has_properties


def test_put_v1_account_password():
    api = DmApiAccount(host="http://localhost:5051")
    mailhog = MailhogApi(host="http://localhost:5025")
    login = "login93"
    password = login + login
    json = Registration(
        login=login,
        email=f"{login}@mail.ru",
        password=login + login
    )

    # Регистрация нового пользователя
    response = api.account.post_v1_account(json=json)

    # Активация зарегистрированного пользователя
    token = mailhog.get_token_from_last_email()
    response = api.account.put_v1_account_token(token=token)
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

    # Смена пароля зарегистрированного пользователя
    json = ChangePassword(
        login=login,
        token=token,
        old_password=password,
        new_password=f"new_{password}",
    )
    response = api.account.put_v1_account_password(json=json)

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
