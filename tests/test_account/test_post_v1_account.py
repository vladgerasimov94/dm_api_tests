import allure
import pytest

from apis.dm_api_account.utilities import random_string


@allure.suite("Тесты на проверку метода POST{host}/v1/account")
class TestsPostV1Account:
    @allure.sub_suite("Позитивные проверки")
    @allure.title("Проверка регистрации и активации пользователя")
    def test_register_and_activate_user(
            self,
            dm_api_facade,
            dm_orm,
            prepare_user,
            assertions,
    ):
        """
        Тест проверяет создание и активацию пользователя в базе данных
        """
        login = prepare_user.login
        email = prepare_user.email
        password = prepare_user.password

        dm_api_facade.account.register_new_user(login=login, email=email, password=password)
        assertions.check_user_was_created(login=login)
        dm_api_facade.account.activate_registered_user(login=login)
        assertions.check_user_was_activated(login=login)
        dm_api_facade.login.login_user(login=login, password=password)

    @pytest.mark.parametrize("login, email, password, status_code, check", [
        ("12", "12@12.ru", "2134544", 201, ""),  # Валидные данные
        ("12", "12@12.ru", random_string(1, 5), 400, {"Password": ["Short"]}),  # Пароль менее либо равен 5 символам
        ("1", "12@12.ru", "2134544", 400, {"Login": ["Short"]}),  # Логин менее 2 символов
        ("12", "12@", "2134544", 400, {"Email": ["Invalid"]}),  # Емейл не содержит доменную часть
        ("12", "12", "2134544", 400, {"Email": ["Invalid"]}),  # Емейл не содержит символ @
    ])
    @allure.sub_suite("Позитивные и негативные проверки")
    @allure.title("Проверка регистрации и активации пользователя с случайными параметрами")
    def test_create_and_activate_user_with_random_params(
            self,
            dm_api_facade,
            dm_orm,
            login,
            email,
            password,
            status_code,
            check,
            assertions,
    ):
        """
        Тест проверяет создание, активацию и логин пользователя в систему, обработку ошибок
        """
        dm_orm.delete_user_by_login(login=login)
        dm_api_facade.mailhog.delete_all_messages()

        response = dm_api_facade.account.register_new_user(
            login=login,
            email=email,
            password=password,
            status_code=status_code,
        )
        if status_code == 201:
            assertions.check_user_was_created(login=login)
            dm_orm.activate_registered_user_by_login(login=login)
            assertions.check_user_was_activated(login=login)
            dm_api_facade.login.login_user(login=login, password=password)
        else:
            assertions.check_response_error(response=response, error_block=check)
