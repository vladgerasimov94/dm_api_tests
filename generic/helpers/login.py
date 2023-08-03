import allure
from requests import Response

from dm_api_account.models import LoginCredentials


class Login:
    def __init__(self, facade):
        from services.dm_api_account import Facade
        self.facade: Facade = facade

    def login_user(
            self,
            login: str,
            password: str,
            remember_me: bool = True,
    ) -> Response:
        with allure.step(f"Авторизация пользователя {login}"):
            response = self.facade.login_api.v1_account_login_post(
                _return_http_data_only=False,
                login_credentials=LoginCredentials(
                    login=login,
                    password=password,
                    remember_me=remember_me,
                ),
            )
            return response

    def get_auth_token(
            self,
            login: str,
            password: str,
            remember_me: bool = True,
    ) -> dict[str, str]:
        with allure.step(f"Получение авторизационного токена для пользователя {login}"):
            response = self.login_user(
                login=login,
                password=password,
                remember_me=remember_me,
            )
            token = response[2]["X-Dm-Auth-Token"]
            return token

    def logout_user(
            self,
            **kwargs
    ) -> Response:
        with allure.step("Разлогин пользователя с текущего устройства"):
            response = self.facade.login_api.v1_account_login_delete(**kwargs)
            return response

    def logout_user_from_all_devices(
            self,
            **kwargs
    ) -> Response:
        with allure.step("Разлогин пользователя со всех устройств"):
            response = self.facade.login_api.v1_account_login_all_delete(**kwargs)
            return response
