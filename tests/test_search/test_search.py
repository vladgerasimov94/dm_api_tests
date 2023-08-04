import pprint

import pytest
from betterproto import Casing
from apis.dm_api_search_async import SearchRequest, SearchEntityType


def test_search(grpc_search, prepare_user, dm_api_facade, dm_orm):
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
    dm_api_facade.forum.set_headers(headers=token)

    dm_api_facade.forum.post_new_topic(topic_id="Общий", topic_title="test_post", topic_description="bla bla bla")

    response = grpc_search.search(
        query="test_post",
        skip=0,
        size=10,
        search_across=["FORUM_TOPIC"],
    )


@pytest.mark.asyncio
async def test_search_async(grpc_search_async, prepare_user, dm_api_facade, dm_orm):
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
    dm_api_facade.forum.set_headers(headers=token)

    dm_api_facade.forum.post_new_topic(topic_id="Общий", topic_title="test_post123", topic_description="bla bla blaaaa")

    response = await grpc_search_async.search(
        search_request=SearchRequest(
            query="test_post",
            skip=0,
            size=10,
            search_across=[SearchEntityType.FORUM_TOPIC],
        )
    )
    pprint.pprint(response.to_dict(casing=Casing.SNAKE))
