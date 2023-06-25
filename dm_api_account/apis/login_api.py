from requests import Response
from requests import session

from ..models.login_credentials_model import login_credentials_model


class LoginApi:
    def __init__(self, host: str, headers: dict | None = None) -> None:
        self.host = host
        self.session = session()
        if headers:
            self.session.headers.update(headers)

    def post_v1_account_login(self, json: login_credentials_model, **kwargs) -> Response:
        """
        Authenticate via credentials
        :param json: login_credentials_model
        :return:
        """
        response = self.session.post(
            url=f"{self.host}/v1/account/login",
            json=json,
            **kwargs
        )
        return response

    def delete_v1_account_login(self, **kwargs) -> Response:
        """
        Logout as current user
        :return:
        """
        response = self.session.delete(
            url=f"{self.host}/v1/account/login",
            **kwargs
        )
        return response

    def delete_v1_account_login_all(self, **kwargs) -> Response:
        """
        Logout from every device
        :return:
        """
        response = self.session.delete(
            url=f"{self.host}/v1/account/login/all",
            **kwargs
        )
        return response
