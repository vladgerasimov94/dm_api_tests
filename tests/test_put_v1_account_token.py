from services.dm_api_account import DmApiAccount


def test_put_v1_account_token():
    api = DmApiAccount(host="http://localhost:5051")
    token = "2c053603-d51d-419f-8832-cae0bf0f52f3"
    response = api.account.put_v1_account_token(token=token)
    print(response)
