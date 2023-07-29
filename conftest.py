from collections import namedtuple

import allure
import structlog
import pytest
from vyper import v
from pathlib import Path

from generic.assertions.post_v1_account import AssertionsPostV1Account
from generic.helpers.mailhog import MailhogApi
from generic.helpers.orm_db import OrmDatabase
from services.dm_api_account import Facade
from data.post_v1_account import PostV1AccountData as data

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)
    ]
)


@pytest.fixture
def mailhog() -> MailhogApi:
    return MailhogApi(host=v.get("service.mailhog"))


@pytest.fixture
def dm_api_facade(mailhog) -> Facade:
    return Facade(host=v.get("service.dm_api_account"), mailhog=mailhog)


@pytest.fixture
def dm_orm():
    orm = OrmDatabase(
        user=v.get("database.dm3_5.user"),
        password=v.get("database.dm3_5.password"),
        host=v.get("database.dm3_5.host"),
        database=v.get("database.dm3_5.database"),
    )
    yield orm
    orm.db.close_connection()


@pytest.fixture
@allure.step("Подготовка тестового пользователя")
def prepare_user(dm_api_facade, dm_orm):
    user_data = namedtuple("User", "login, email, password")
    user = user_data(login=data.login, email=data.email, password=data.password)
    dm_orm.delete_user_by_login(login=user.login)
    dataset = dm_orm.get_user_by_login(login=user.login)
    assert len(dataset) == 0
    dm_api_facade.mailhog.delete_all_messages()

    return user


options = (
    "service.dm_api_account",
    "service.mailhog",
    "database.dm3_5.host",
)  # 1. Создаем список опций, которые можем динамически менять


@pytest.fixture(autouse=True)
def set_config(request):
    config = Path(__file__).parent.joinpath("config")  # 3. С помощью Pathlib получаем путь к папке с конфигом
    config_name = request.config.getoption("--env")  # 4. Указываем имя конфига
    v.set_config_name(config_name)  # 5. В виртуальное окружение указываем: имя конфига,
    v.add_config_path(config)  # путь,
    v.read_in_config()  # вычитываем в окружение
    for option in options:  # и устанавливаем отдельные опции и значения
        v.set(option, request.config.getoption(f"--{option}"))


def pytest_addoption(parser):
    parser.addoption(
        "--env", action="store", default="server"  # 2. Изменяем опцию env, которая читает полностью конфиг
    )
    for option in options:
        parser.addoption(f"--{option}", action="store", default=None)


@pytest.fixture
def assertions(dm_orm):
    return AssertionsPostV1Account(dm_orm)
