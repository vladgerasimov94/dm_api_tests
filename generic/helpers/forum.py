import allure

from apis.dm_api_forum.models.topic_envelope_model import TopicEnvelope
from apis.dm_api_forum.models.topic_model import Topic
from apis.dm_api_forum.models.topic_model import Forum as ForumModel


class Forum:
    def __init__(self, facade) -> None:
        from services.dm_api_account import Facade
        self.facade: Facade = facade

    def set_headers(self, headers: dict) -> None:
        """
        set headers for account helper
        :param headers:
        :return:
        """
        with allure.step("Обновление заголовков для сессии forum_api"):
            self.facade.forum_api.client.session.headers.update(headers)

    def post_new_topic(
            self,
            topic_id: str,
            topic_title: str,
            topic_description: str,
            unread_topics_count: int = 0,
            status_code: int = 201
    ) -> TopicEnvelope:
        """
        Post new topic
        :param topic_id:
        :param topic_title:
        :param topic_description:
        :param unread_topics_count:
        :param status_code:
        :return:
        """
        with allure.step("Пост новой темы в форуме"):
            json = Topic(
                forum=(
                    ForumModel(
                        id=topic_id,
                        unread_topics_count=unread_topics_count,
                    )
                ),
                title=topic_title,
                description=topic_description,
            ).model_dump(by_alias=True, exclude_none=True)

            response = self.facade.forum_api.post_v1_fora_topics(
                json=json, status_code=status_code
            )
            return response
