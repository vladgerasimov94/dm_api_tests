import requests

from dm_api_account.models.change_password_model import ChangePasswordModel
from dm_api_account.models.registration_model import RegistrationModel
from services.dm_api_account import DmApiAccount
from services.mailhog import MailhogApi


def test_put_v1_account_password():
    api = DmApiAccount(host="http://localhost:5051")
    mailhog = MailhogApi(host="http://localhost:5025")
    login = "login61"
    password = login + login
    json = RegistrationModel(
        login=login,
        email=f"{login}@mail.ru",
        password=login + login
    )

    # Регистрация нового пользователя
    response = api.account.post_v1_account(json=json)
    assert response.status_code == requests.codes.created, f"Expected status code: 201, got: {response.status_code}"

    # Активация зарегистрированного пользователя
    token = mailhog.get_token_from_last_email()
    response = api.account.put_v1_account_token(token=token)
    assert response.status_code == requests.codes.ok

    # Смена пароля зарегистрированного пользователя
    json = ChangePasswordModel(
        login=login,
        token=token,
        old_password=password,
        new_password=f"new_{password}",
    )
    response = api.account.put_v1_account_password(json=json)
    assert response.status_code == requests.codes.ok
