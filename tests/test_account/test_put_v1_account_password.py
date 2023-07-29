def test_put_v1_account_password(dm_api_facade, dm_orm, prepare_user):
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
    dm_api_facade.account.set_headers(headers=token)

    old_password_hash = dm_orm.get_password_hash_by_login(login=login)
    dm_api_facade.account.reset_registered_user_password(login=login, email=email)

    dm_api_facade.account.change_registered_user_password(
        login=login,
        old_password=password,
        new_password=f"new_{password}"
    )
    new_password_hash = dm_orm.get_password_hash_by_login(login=login)
    assert new_password_hash != old_password_hash
