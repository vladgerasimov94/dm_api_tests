from generic.helpers.orm_db import OrmDatabase
from services.dm_api_account import Facade
import structlog
from dm_api_account.models.user_envelope_model import UserRole, Rating
from hamcrest import assert_that, has_properties

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)
    ]
)


def test_put_v1_account_token():
    api = Facade(host="http://localhost:5051")
    orm = OrmDatabase(user="postgres", password="admin", host="localhost", database="dm3.5")

    login = "login123"
    email = f"{login}@mail.ru"
    password = login + login

    orm.delete_user_by_login(login=login)
    dataset = orm.get_user_by_login(login=login)
    assert len(dataset) == 0

    api.mailhog.delete_all_messages()

    api.account.register_new_user(
        login=login,
        email=email,
        password=password
    )

    dataset = orm.get_user_by_login(login=login)
    for row in dataset:
        assert row.Login == login
        assert row.Activated is False

    response = api.account.activate_registered_user(login=login)

    dataset = orm.get_user_by_login(login=login)
    for row in dataset:
        assert row.Activated is True

    assert_that(response.resource, has_properties(
        {
            "login": login,
            "roles": [UserRole.GUEST, UserRole.PLAYER],
            "rating": Rating(
                enabled=True,
                quality=0,
                quantity=0
            )
        }
    ))
