import pytest

from dm_api_account.utilities import random_string
from hamcrest import assert_that, equal_to


@pytest.mark.parametrize("login, email, password, status_code, check", [
    ("12", "12@12.ru", "2134544", 201, ""),  # Валидные данные
    ("12", "12@12.ru", random_string(1, 5), 400, {"Password": ["Short"]}),  # Пароль менее либо равен 5 символам
    ("1", "12@12.ru", "2134544", 400, {"Login": ["Short"]}),  # Логин менее 2 символов
    ("12", "12@", "2134544", 400, {"Email": ["Invalid"]}),  # Емейл не содержит доменную часть
    ("12", "12", "2134544", 400, {"Email": ["Invalid"]}),  # Емейл не содержит символ @
])
def test_create_and_activate_user_with_random_params(
        dm_api_facade,
        dm_orm,
        login,
        email,
        password,
        status_code,
        check
):
    dm_orm.delete_user_by_login(login=login)
    dm_api_facade.mailhog.delete_all_messages()

    response = dm_api_facade.account.register_new_user(
        login=login,
        email=email,
        password=password,
        status_code=status_code,
    )
    if status_code == 201:
        dm_orm.activate_registered_user_by_login(login=login)

        dataset = dm_orm.get_user_by_login(login=login)
        for row in dataset:
            assert row.Activated is True

        dm_api_facade.login.login_user(login=login, password=password)
    else:
        assert_that(response.json()["errors"], equal_to(check))
