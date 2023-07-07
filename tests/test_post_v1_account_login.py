from datetime import datetime

from hamcrest import assert_that, instance_of, has_properties

from dm_api_account.models.login_credentials_model import LoginCredentials
from dm_api_account.models.registration_model import Registration
from dm_api_account.models.user_envelope_model import UserRole, Rating
from services.dm_api_account import DmApiAccount
import structlog

from services.mailhog import MailhogApi

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)
    ]
)


def test_post_v1_account_login():
    mailhog = MailhogApi(host="http://localhost:5025")
    api = DmApiAccount(host="http://localhost:5051")
    login = "login96"
    password = login + login
    json = Registration(
        login=login,
        email=f"{login}@mail.ru",
        password=password
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

    # Аутентификация пользователя по кредам
    json_login = LoginCredentials(
        login=login,
        password=password,
        rememberMe=True
    )
    response = api.login.post_v1_account_login(json=json_login)

    assert_that(response.resource, has_properties(
        {
            "login": login,
            "roles": [UserRole.GUEST, UserRole.PLAYER],
            "registration": instance_of(datetime)
        }
    ))
