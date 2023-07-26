import allure
from hamcrest import assert_that, is_, equal_to
from generic.helpers.orm_db import OrmDatabase


class AssertionsPostV1Account:
    def __init__(self, orm: OrmDatabase):
        self.orm = orm

    def check_user_was_created(self, login):
        with allure.step(f"Проверка создания пользователя {login}"):
            dataset = self.orm.get_user_by_login(login=login)
            for row in dataset:
                assert_that(row.Activated, is_(False))
                assert_that(row.Login, equal_to(login))

    def check_user_was_activated(self, login):
        with allure.step(f"Проверка успешной активации пользователя {login}"):
            dataset = self.orm.get_user_by_login(login=login)
            for row in dataset:
                assert_that(row.Activated, is_(True))

    @staticmethod
    def check_response_error(response, error_block: dict):
        with allure.step(f"Проверка наличия в респонсе блока с текстом ошибки: {error_block}"):
            assert_that(response.json()["errors"], equal_to(error_block))
