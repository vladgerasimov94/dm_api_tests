import requests

from dm_api_account.models.login_credentials_model import LoginCredentialsModel
from dm_api_account.models.registration_model import RegistrationModel
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
    login = "login63"
    password = login + login
    json = RegistrationModel(
        login=login,
        email=f"{login}@mail.ru",
        password=password
    )
    # Регистрация нового пользователя
    response = api.account.post_v1_account(json=json)
    assert response.status_code == requests.codes.created, f"Expected status code: 201, got: {response.status_code}"
    # Активация зарегистрированного пользователя
    token = mailhog.get_token_from_last_email()
    response = api.account.put_v1_account_token(token=token)
    assert response.status_code == requests.codes.ok

    # Аутентификация пользователя по кредам
    json_login = LoginCredentialsModel(
        login=login,
        password=password,
        rememberMe=True
    )
    response = api.login.post_v1_account_login(json=json_login)
    assert response.status_code == requests.codes.ok
