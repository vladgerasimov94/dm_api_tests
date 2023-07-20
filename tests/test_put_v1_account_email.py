def test_put_v1_account_email(dm_api_facade, dm_orm, prepare_user):
    login = prepare_user.login
    email = prepare_user.email
    password = prepare_user.password
    new_email = f"new_{email}"

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

    dm_api_facade.account.change_registered_user_email(
        login=login,
        password=password,
        email=new_email
    )
    dataset = dm_orm.get_user_by_login(login=login)
    for row in dataset:
        assert row.Login == login
        assert row.Email == new_email
