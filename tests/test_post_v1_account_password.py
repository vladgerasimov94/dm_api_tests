import requests

from dm_api_account.models.reset_password_model import ResetPasswordModel
from services.dm_api_account import DmApiAccount


def test_post_v1_account_password():
    api = DmApiAccount(host="http://localhost:5051")
    login = "login41"
    json = ResetPasswordModel(
        login=login,
        email=f"{login}@mail.ru"
    )
    response = api.account.post_v1_account_password(json=json)
    assert response.status_code == requests.codes.ok
