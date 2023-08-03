import allure
from requests import Response

from dm_api_account.models import Registration, UserEnvelope, UserDetailsEnvelope, ChangePassword, ResetPassword, \
    ChangeEmail
from generic.helpers.mailhog import TokenType


class Account:
    def __init__(self, facade) -> None:
        from services.dm_api_account import Facade
        self.facade: Facade = facade

    def register_new_user(
            self,
            login: str,
            email: str,
            password: str,
    ) -> Response:
        with allure.step(f"Регистрация нового пользователя '{login}'"):
            response = self.facade.account_api.register(
                registration=Registration(
                    login=login,
                    email=email,
                    password=password
                ),
            )
            return response

    def activate_registered_user(
            self,
            login: str,
    ) -> Response | UserEnvelope:
        with allure.step("Активация зарегистрированного пользователя"):
            token = self.facade.mailhog.get_token_by_login(login=login, token_type=TokenType.ACTIVATE)
            response = self.facade.account_api.activate(
                token=token,
            )
            return response

    def get_current_user_info(
            self,
            **kwargs
    ) -> Response | UserDetailsEnvelope:
        with allure.step("Получение информации о текущем пользователе"):
            response = self.facade.account_api.get_current(
                **kwargs
            )
            return response

    def change_registered_user_password(
            self,
            login: str,
            old_password: str,
            new_password: str,
            **kwargs
    ) -> Response | UserEnvelope:
        with allure.step(f"Смена пароля для зарегистрированного пользователя {login}"):
            reset_password_token = self.facade.mailhog.get_token_by_login(
                login=login,
                token_type=TokenType.RESET_PASSWORD
            )
            json = ChangePassword(
                login=login,
                token=reset_password_token,
                old_password=old_password,
                new_password=new_password
            )
            response = self.facade.account_api.change_password(change_password=json, **kwargs)
            return response

    def change_registered_user_email(
            self,
            login: str,
            password: str,
            email: str,
            **kwargs
    ) -> Response | UserEnvelope:
        with allure.step(f"Смена емейла для зарегистрированного пользователя {login}"):
            json = ChangeEmail(
                login=login,
                password=password,
                email=email
            )
            response = self.facade.account_api.change_email(change_email=json, **kwargs)
            return response

    def reset_registered_user_password(
            self,
            login: str,
            email: str,
            **kwargs
    ) -> Response | UserEnvelope:
        with allure.step(f"Сброс пароля для зарегистрированного пользователя {login}"):
            json = ResetPassword(
                login=login,
                email=email
            )
            response = self.facade.account_api.reset_password(reset_password=json, **kwargs)
            return response
