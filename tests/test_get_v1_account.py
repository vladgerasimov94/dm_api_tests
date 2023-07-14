import time
from datetime import datetime

import structlog
from hamcrest import assert_that, has_properties, instance_of

from dm_api_account.models.user_details_envelope_model import UserRole
from generic.helpers.orm_db import OrmDatabase
from services.dm_api_account import Facade

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)
    ]
)


def test_get_v1_account():
    api = Facade(host="http://localhost:5051")
    orm = OrmDatabase(user="postgres", password="admin", host="localhost", database="dm3.5")

    login = "login119"
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
    dataset = orm.get_user_by_login(login=login)
    for row in dataset:
        assert row.Login == login
        assert row.Activated is False

    orm.activate_registered_user_by_login(login=login)
    time.sleep(2)
    dataset = orm.get_user_by_login(login=login)
    for row in dataset:
        assert row.Activated is True

    token = api.login.get_auth_token(login=login, password=password)
    api.account.set_headers(headers=token)

    response = api.account.get_current_user_info()
    assert_that(response.resource, has_properties(
        {
            "login": login,
            "roles": [UserRole.GUEST, UserRole.PLAYER],
            "registration": instance_of(datetime)
        }
    ))
