import time

import structlog

from generic.helpers.orm_db import OrmDatabase
from services.dm_api_account import Facade

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)
    ]
)


def test_delete_v1_account_login_all():
    api = Facade(host="http://localhost:5051")
    orm = OrmDatabase(user="postgres", password="admin", host="localhost", database="dm3.5")

    login = "login120"
    email = f"{login}@mail.ru"
    password = login + login

    orm.delete_user_by_login(login=login)
    dataset = orm.get_user_by_login(login=login)
    assert len(dataset) == 0

    api.mailhog.delete_all_messages()

    api.account.register_new_user(
        login=login,
        email=email,
        password=password
    )

    orm.activate_registered_user_by_login(login=login)
    time.sleep(2)
    dataset = orm.get_user_by_login(login=login)
    for row in dataset:
        assert row.Activated is True

    token = api.login.get_auth_token(login=login, password=password)
    api.login.set_headers(headers=token)
    api.login.logout_user_from_all_devices()
