from datetime import datetime

from hamcrest import assert_that, equal_to, instance_of, contains_exactly

from dm_api_account.models.login_credentials_model import LoginCredentials
from dm_api_account.models.registration_model import Registration
from dm_api_account.models.user_envelope_model import UserRole
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
    login = "login76"
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

    assert_that(response.resource.login, equal_to(login))
    assert_that(response.resource.rating.quality, equal_to(0))
    assert_that(response.resource.rating.enabled, equal_to(True))

    # Аутентификация пользователя по кредам
    json_login = LoginCredentials(
        login=login,
        password=password,
        rememberMe=True
    )
    response = api.login.post_v1_account_login(json=json_login)

    assert_that(response.resource.registration, instance_of(datetime))
    assert_that(response.resource.login, equal_to(login))
    assert_that(response.resource.roles, contains_exactly(UserRole.GUEST, UserRole.PLAYER))
