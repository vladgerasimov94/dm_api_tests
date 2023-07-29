import allure
from requests import Response

from apis.dm_api_account.models import Registration, UserEnvelope, UserDetailsEnvelope, ChangePassword, ResetPassword, \
    ChangeEmail
from generic.helpers.mailhog import TokenType


class Account:
    def __init__(self, facade) -> None:
        from services.dm_api_account import Facade
        self.facade: Facade = facade

    def set_headers(self, headers: dict) -> None:
        """
        set headers for account helper
        :param headers:
        :return:
        """
        with allure.step("Обновление заголовков для сессии account_api"):
            self.facade.account_api.client.session.headers.update(headers)

    def register_new_user(
            self,
            login: str,
            email: str,
            password: str,
            status_code: int = 201
    ) -> Response:
        with allure.step(f"Регистрация нового пользователя '{login}'"):
            response = self.facade.account_api.post_v1_account(
                json=Registration(
                    login=login,
                    email=email,
                    password=password
                ),
                status_code=status_code
            )
            return response

    def activate_registered_user(
            self,
            login: str,
            status_code: int = 200
    ) -> Response | UserEnvelope:
        with allure.step("Активация зарегистрированного пользователя"):
            token = self.facade.mailhog.get_token_by_login(login=login, token_type=TokenType.ACTIVATE)
            response = self.facade.account_api.put_v1_account_token(
                token=token,
                status_code=status_code
            )
            return response

    def get_current_user_info(
            self,
            status_code: int = 200,
            **kwargs
    ) -> Response | UserDetailsEnvelope:
        with allure.step("Получение информации о текущем пользователе"):
            response = self.facade.account_api.get_v1_account(
                status_code=status_code,
                **kwargs
            )
            return response

    def change_registered_user_password(
            self,
            login: str,
            old_password: str,
            new_password: str,
            status_code: int = 200,
            **kwargs
    ) -> Response | UserEnvelope:
        with allure.step(f"Смена пароля для зарегистрированного пользователя {login}"):
            reset_password_token = self.facade.mailhog.get_token_by_login(login=login,
                                                                          token_type=TokenType.RESET_PASSWORD)
            json = ChangePassword(
                login=login,
                token=reset_password_token,
                old_password=old_password,
                new_password=new_password
            )
            response = self.facade.account_api.put_v1_account_password(json=json, status_code=status_code, **kwargs)
            return response

    def change_registered_user_email(
            self,
            login: str,
            password: str,
            email: str,
            status_code: int = 200,
            **kwargs
    ) -> Response | UserEnvelope:
        with allure.step(f"Смена емейла для зарегистрированного пользователя {login}"):
            json = ChangeEmail(
                login=login,
                password=password,
                email=email
            )
            response = self.facade.account_api.put_v1_account_email(json=json, status_code=status_code, **kwargs)
            return response

    def reset_registered_user_password(
            self,
            login: str,
            email: str,
            status_code: int = 200,
            **kwargs
    ) -> Response | UserEnvelope:
        with allure.step(f"Сброс пароля для зарегистрированного пользователя {login}"):
            json = ResetPassword(
                login=login,
                email=email
            )
            response = self.facade.account_api.post_v1_account_password(json=json, status_code=status_code, **kwargs)
            return response
