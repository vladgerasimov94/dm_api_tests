import allure
from requests import Response

from dm_api_account.models import LoginCredentials


class Login:
    def __init__(self, facade):
        from services.dm_api_account import Facade
        self.facade: Facade = facade

    def set_headers(self, headers: dict) -> None:
        """
        set headers for login helper
        :param headers:
        :return:
        """
        self.facade.login_api.client.session.headers.update(headers)

    def login_user(
            self,
            login: str,
            password: str,
            remember_me: bool = True,
            status_code: int = 200
    ) -> Response:
        with allure.step(f"Авторизация пользователя {login}"):
            response = self.facade.login_api.post_v1_account_login(
                json=LoginCredentials(
                    login=login,
                    password=password,
                    remember_me=remember_me,
                ),
                status_code=status_code
            )
            return response

    def get_auth_token(
            self,
            login: str,
            password: str,
            remember_me: bool = True,
            status_code: int = 200
    ) -> dict[str, str]:
        with allure.step(f"Получение авторизационного токена для пользователя {login}"):
            response = self.login_user(
                login=login,
                password=password,
                remember_me=remember_me,
                status_code=status_code
            )
            token = {"X-Dm-Auth-Token": response.headers["X-Dm-Auth-Token"]}
            return token

    def logout_user(
            self,
            status_code: int = 204,
            **kwargs
    ) -> Response:
        with allure.step("Разлогин пользователя с текущего устройства"):
            response = self.facade.login_api.delete_v1_account_login(status_code=status_code, **kwargs)
            return response

    def logout_user_from_all_devices(
            self,
            status_code: int = 204,
            **kwargs
    ) -> Response:
        with allure.step("Разлогин пользователя со всех устройств"):
            response = self.facade.login_api.delete_v1_account_login_all(status_code=status_code, **kwargs)
            return response
