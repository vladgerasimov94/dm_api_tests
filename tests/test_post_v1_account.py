import time

from hamcrest import assert_that, has_length

from generic.helpers.dm_db import DmDatabase
from services.dm_api_account import Facade
import structlog

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)
    ]
)


def test_post_v1_account():
    api = Facade(host="http://localhost:5051")
    db = DmDatabase(user="postgres", password="admin", host="localhost", database="dm3.5")

    login = "login103"
    email = f"{login}@mail.ru"
    password = login + login

    db.delete_user_by_login(login=login)
    dataset = db.get_user_by_login(login=login)
    assert_that(dataset, has_length(0))

    api.mailhog.delete_all_messages()

    api.account.register_new_user(
        login=login,
        email=email,
        password=password
    )
    dataset = db.get_user_by_login(login=login)
    for row in dataset:
        assert row["Login"] == login, f"User {login} not registered"
        assert row["Activated"] is False, f"User {login} was activated"

    db.activate_registered_user_by_login(login=login)

    time.sleep(2)
    dataset = db.get_user_by_login(login=login)
    for row in dataset:
        assert row["Activated"] is True, f"User {login} not activated"

    api.login.login_user(login=login, password=password)
