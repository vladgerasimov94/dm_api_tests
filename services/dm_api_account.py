from dm_api_account.apis.account_api import AccountApi
from dm_api_account.apis.login_api import LoginApi


class DmApiAccount:
    def __init__(self, host: str, headers: dict | None = None) -> None:
        self.account = AccountApi(host=host, headers=headers)
        self.login = LoginApi(host=host, headers=headers)
