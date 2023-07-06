from hamcrest import assert_that, equal_to, has_property

from dm_api_account.models.user_envelope_model import UserRole
from services.dm_api_account import DmApiAccount
from services.mailhog import MailhogApi
import structlog
from dm_api_account.models.registration_model import Registration

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)
    ]
)


def test_post_v1_account():
    mailhog = MailhogApi(host="http://localhost:5025")
    api = DmApiAccount(host="http://localhost:5051")
    login = "login72"
    json = Registration(
        login=login,
        email=f"{login}@mail.ru",
        password=login + login
    )
    # Регистрация нового пользователя
    response = api.account.post_v1_account(json=json)

    # Активация зарегистрированного пользователя
    token = mailhog.get_token_from_last_email()
    response = api.account.put_v1_account_token(token=token)

    assert_that(response.resource, has_property(
        "roles", [UserRole.GUEST, UserRole.PLAYER]
    ))
    assert_that(response.resource.login, equal_to(login))
    assert_that(response.resource.rating.quality, equal_to(0))
    assert_that(response.resource.rating.enabled, equal_to(True))
