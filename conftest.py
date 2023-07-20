from collections import namedtuple

import pytest

from generic.helpers.mailhog import MailhogApi
from generic.helpers.orm_db import OrmDatabase
from services.dm_api_account import Facade
import structlog

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)
    ]
)


@pytest.fixture
def mailhog() -> MailhogApi:
    return MailhogApi(host="http://localhost:5025")


@pytest.fixture
def dm_api_facade(mailhog) -> Facade:
    return Facade(host="http://localhost:5051", mailhog=mailhog)


@pytest.fixture
def dm_orm():
    orm = OrmDatabase(user="postgres", password="admin", host="localhost", database="dm3.5")
    yield orm
    orm.db.close_connection()


@pytest.fixture
def prepare_user(dm_api_facade, dm_orm):
    user_data = namedtuple("User", "login, email, password")
    user = user_data(login="login103", email="login103@mail.ru", password="login103login103")
    dm_orm.delete_user_by_login(login=user.login)
    dataset = dm_orm.get_user_by_login(login=user.login)
    assert len(dataset) == 0
    dm_api_facade.mailhog.delete_all_messages()

    return user
