import requests

from services.dm_api_account import DmApiAccount
from services.mailhog import MailhogApi
import structlog
from dm_api_account.models.registration_model import RegistrationModel

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)
    ]
)


def test_post_v1_account():
    mailhog = MailhogApi(host="http://localhost:5025")
    api = DmApiAccount(host="http://localhost:5051")
    login = "login58"
    json = RegistrationModel(
        login=login,
        email=f"{login}@mail.ru",
        password=login + login
    )
    # # Регистрация нового пользователя
    response = api.account.post_v1_account(json=json)
    assert response.status_code == requests.codes.created, f"Expected status code: 201, got: {response.status_code}"
    # Активация зарегистрированного пользователя
    token = mailhog.get_token_from_last_email()
    response = api.account.put_v1_account_token(token=token)
    assert response.status_code == requests.codes.ok
