import allure


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

    def post_new_topic(self, forum_id, json, status_code: int = 201):
        with allure.step("Пост новой темы в форуме"):
            self.facade.forum_api.post_v1_fora_topics(
                forum_id=forum_id, json=json, status_code=status_code
            )
