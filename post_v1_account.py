import requests


def post_v1_account():
    """
    Register new user
    :return:
    """
    url = "http://localhost:5051/v1/account"

    payload = {
        "login": "login7",
        "email": "login7@mail.ru",
        "password": "login7login7"
    }
    headers = {
        'X-Dm-Auth-Token': '<string>',
        'X-Dm-Bb-Render-Mode': '<string>',
        'Content-Type': 'application/json',
        'Accept': 'text/plain'
    }

    response = requests.request(
        method="POST",
        url=url,
        headers=headers,
        json=payload
    )
    return response


response = post_v1_account()
print(response.request)
print(response.content)
print(response.url)
print(response.status_code)
print(response.json()["type"])
