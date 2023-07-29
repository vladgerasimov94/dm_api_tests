import json
import time
from dataclasses import dataclass
from enum import Enum, auto
from time import sleep

import allure
from requests import Response
from common_libs.restclient.restclient import Restclient


@dataclass
class EmailBodyInfo:
    token_name: str
    link_type: str


class TokenType(Enum):
    RESET_PASSWORD = auto()
    ACTIVATE = auto()


class MailhogApi:
    def __init__(self, host: str = "http://localhost:5025") -> None:
        self.host = host
        self.client = Restclient(host=host)

    # @decorator
    def get_api_v2_messages(self, limit: int = 50) -> Response:
        """
        Get messages by limit
        :param limit:
        :return:
        """
        with allure.step(f"Получение списка сообщений из {limit} шт."):
            response = self.client.get(
                path="/api/v2/messages",
                params={
                    'limit': limit
                }
            )

        return response

    def get_token_from_last_email(self) -> str:
        """
        Get user activation token from last email
        :return:
        """
        with allure.step("Получение токена активации из последнего письма"):
            sleep(2)
            emails = self.get_api_v2_messages(limit=1).json()
            token_url = json.loads(emails["items"][0]["Content"]["Body"])["ConfirmationLinkUrl"]
            token = token_url.split("/")[-1]
            return token

    @staticmethod
    def _get_token_info_by_type(token_type: TokenType) -> EmailBodyInfo:
        with allure.step("Получение деталей о токене по его типу"):
            match token_type:
                case token_type.RESET_PASSWORD:
                    return EmailBodyInfo(token_name="password", link_type="ConfirmationLinkUri")
                case token_type.ACTIVATE:
                    return EmailBodyInfo(token_name="activate", link_type="ConfirmationLinkUrl")

    def get_token_by_login(self, login: str, token_type: TokenType, attempt: int = 5) -> str:
        with allure.step(f"Получение токена {'активации' if token_type is TokenType.ACTIVATE else 'сброса пароля'}"):
            token_info = self._get_token_info_by_type(token_type)
            if attempt == 0:
                raise AssertionError(f"Не удалось получить письмо с логином {login}")
            emails = self.get_api_v2_messages(limit=100).json()["items"]
            for email in emails:
                user_data = json.loads(email["Content"]["Body"])
                if token_info.link_type in user_data:
                    confirmation_link_url = user_data[token_info.link_type]
                    if login == user_data.get("Login") and token_info.token_name in confirmation_link_url:
                        token = confirmation_link_url.split("/")[-1]
                        return token
            time.sleep(2)
            return self.get_token_by_login(login=login, token_type=token_type, attempt=attempt - 1)

    def delete_all_messages(self):
        with allure.step("Удаление всех сообщений из почтового клиента Mailhog"):
            response = self.client.delete(path="/api/v1/messages")
            return response
