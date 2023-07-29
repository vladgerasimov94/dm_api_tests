from datetime import datetime
from apis.dm_api_account.models.user_envelope_model import UserRole
from hamcrest import assert_that, instance_of, has_properties


def test_post_v1_account_password(dm_api_facade, dm_orm, prepare_user):
    login = prepare_user.login
    email = prepare_user.email
    password = prepare_user.password

    dm_api_facade.account.register_new_user(
        login=login,
        email=email,
        password=password
    )
    dm_orm.activate_registered_user_by_login(login=login)

    response = dm_api_facade.account.reset_registered_user_password(login=login, email=email)
    assert_that(response.resource, has_properties(
        {
            "login": login,
            "roles": [UserRole.GUEST, UserRole.PLAYER],
            "registration": instance_of(datetime)
        }
    ))
