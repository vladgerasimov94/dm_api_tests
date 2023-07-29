from apis.dm_api_account.apis.account_api import AccountApi
from apis.dm_api_account.apis.login_api import LoginApi
from generic.helpers.account import Account
from generic.helpers.login import Login


class Facade:
    def __init__(self, host: str, mailhog=None, headers: dict | None = None) -> None:
        self.account_api = AccountApi(host=host, headers=headers)
        self.login_api = LoginApi(host=host, headers=headers)
        self.mailhog = mailhog
        self.account = Account(self)
        self.login = Login(self)

