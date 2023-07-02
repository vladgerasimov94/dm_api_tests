import requests

from dm_api_account.models.change_email_model import ChangeEmailModel
from dm_api_account.models.registration_model import RegistrationModel
from services.dm_api_account import DmApiAccount
from services.mailhog import MailhogApi
import structlog

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)
    ]
)


def test_put_v1_account_email():
    mailhog = MailhogApi(host="http://localhost:5025")
    api = DmApiAccount(host="http://localhost:5051")
    login = "login62"
    password = login + login
    email = f"{login}@mail.ru"
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

    # Изменение почты зарегистрированного пользователя
    json = ChangeEmailModel(
        login=login,
        password=password,
        email=f"new_{email}",
    )
    response = api.account.put_v1_account_email(json=json)
    assert response.status_code == requests.codes.ok
