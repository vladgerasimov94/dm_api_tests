import allure
from requests import Response

from apis.dm_api_forum.models.topic_envelope_model import TopicEnvelope
from apis.dm_api_forum.models.topic_model import Topic
from common_libs.restclient.restclient import Restclient
from apis.dm_api_account.utilities import validate_status_code, validate_request_json


class ForumApi:
    def __init__(self, host: str, headers: dict | None = None) -> None:
        self.host = host
        self.client = Restclient(host=host, headers=headers)
        if headers:
            self.client.session.headers.update(headers)

    def post_v1_fora_topics(
            self,
            json: Topic,
            status_code: int = 201,
            **kwargs
    ) -> Response | TopicEnvelope:
        """
        Post new topic
        :param json:
        :param status_code:
        :param kwargs:
        :return:
        """
        with allure.step("Пост новой темы в форуме"):
            response = self.client.post(
                path=f"/v1/fora/{json['forum']['id']}/topics",
                json=validate_request_json(json),
                **kwargs,
            )
            validate_status_code(response=response, status_code=status_code)
            if response.status_code == status_code:
                return TopicEnvelope(**response.json())
            return response
