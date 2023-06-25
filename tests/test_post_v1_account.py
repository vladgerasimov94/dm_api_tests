import requests

from services.dm_api_account import DmApiAccount


def test_post_v1_account():
    api = DmApiAccount(host="http://localhost:5051")
    json = {
        "login": "login11",
        "email": "login11@mail.ru",
        "password": "login11login11"
    }
    response_creation = api.account.post_v1_account(json=json)
    assert response_creation.status_code == requests.codes.created, f"User '{json['login']}' is not created"
    # TODO: Get token from mail
    token = "b5731949-f17e-4bd3-8756-d081c6cf0b57"
    response_activation = api.account.put_v1_account_token(token=token)
    assert response_activation.status_code == requests.codes.ok, f"User '{json['login']}' is not activated"
