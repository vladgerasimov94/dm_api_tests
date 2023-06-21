import requests


def put_v1_account_password():
    """
    Change registered user password
    :return:
    """
    url = "http://localhost:5051/v1/account/password"

    payload = {
        "login": "<string>",
        "token": "<uuid>",
        "oldPassword": "<string>",
        "newPassword": "<string>"
    }
    headers = {
        'X-Dm-Auth-Token': '<string>',
        'X-Dm-Bb-Render-Mode': '<string>',
        'Content-Type': 'application/json',
        'Accept': 'text/plain'
    }

    response = requests.request(
        "PUT",
        url,
        headers=headers,
        json=payload
    )
    return response
