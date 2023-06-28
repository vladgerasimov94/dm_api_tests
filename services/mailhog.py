import json
from time import sleep

from requests import Response
from restclient.restclient import Restclient


class MailhogApi:
    def __init__(self, host: str) -> None:
        self.host = host
        self.client = Restclient(host=host)

    def get_api_v2_messages(self, limit: int = 50) -> Response:
        """
        Get messages by limit
        :param limit:
        :return:
        """
        sleep(1)  # Без слипа почти всегда берет предпоследнее письмо, не успевает обновиться
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
        emails = self.get_api_v2_messages(limit=1).json()
        token_url = json.loads(emails["items"][0]["Content"]["Body"])["ConfirmationLinkUrl"]
        token = token_url.split("/")[-1]
        return token
