from datetime import datetime
from hamcrest import assert_that, has_properties, instance_of


def test_get_v1_account(dm_api_facade, dm_orm, prepare_user):
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

    dm_orm.activate_registered_user_by_login(login=login)
    dataset = dm_orm.get_user_by_login(login=login)
    for row in dataset:
        assert row.Activated is True

    token = dm_api_facade.login.get_auth_token(login=login, password=password)

    response = dm_api_facade.account.get_current_user_info(x_dm_auth_token=token)
    assert_that(response.resource, has_properties(
        {
            "login": login,
            "registration": instance_of(datetime)
        }
    ))
