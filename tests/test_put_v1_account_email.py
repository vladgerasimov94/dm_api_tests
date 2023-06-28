import requests

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
    login = "login35"
    email = f"{login}@mail.ru"
    json = {
        "login": login,
        "email": email,
        "password": login + login
    }
    # Регистрация нового пользователя
    response = api.account.post_v1_account(json=json)
    assert response.status_code == requests.codes.created, f"Status code should be equal {requests.codes.created}. " \
                                                           f"Got: {response.status_code}. " \
                                                           f"User '{json['login']}' is not created"
    # Активация зарегистрированного пользователя
    token = mailhog.get_token_from_last_email()
    response = api.account.put_v1_account_token(token=token)
    assert response.status_code == requests.codes.ok

    # Изменение почты зарегистрированного пользователя
    json["email"] = "new_" + email
    response = api.account.put_v1_account_email(json=json)
    assert response.status_code == requests.codes.ok
