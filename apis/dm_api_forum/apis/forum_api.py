import allure
from requests import Response

from common_libs.restclient.restclient import Restclient
from apis.dm_api_account.utilities import validate_status_code


class ForumApi:
    def __init__(self, host: str, headers: dict | None = None) -> None:
        self.host = host
        self.client = Restclient(host=host, headers=headers)
        if headers:
            self.client.session.headers.update(headers)

    def post_v1_fora_topics(
            self,
            forum_id: str,
            json,
            status_code: int = 201,
            **kwargs
    ) -> Response:
        """
        Post new topic
        :param forum_id:
        :param json:
        :param status_code:
        :param kwargs:
        :return:
        """
        with allure.step("Пост новой темы в форуме"):
            response = self.client.post(
                path=f"/v1/fora/{forum_id}/topics",
                json=json,
                **kwargs,
            )
            validate_status_code(response=response, status_code=status_code)
            return response
