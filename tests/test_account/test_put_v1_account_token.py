from apis.dm_api_account.models.user_envelope_model import UserRole, Rating
from hamcrest import assert_that, has_properties


def test_put_v1_account_token(dm_api_facade, dm_orm, prepare_user):
    login = prepare_user.login
    email = prepare_user.email
    password = prepare_user.password

    dm_api_facade.account.register_new_user(
        login=login,
        email=email,
        password=password
    )

    dataset = dm_orm.get_user_by_login(login=login)
    for row in dataset:
        assert row.Login == login
        assert row.Activated is False

    response = dm_api_facade.account.activate_registered_user(login=login)

    dataset = dm_orm.get_user_by_login(login=login)
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
