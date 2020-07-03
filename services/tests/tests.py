import pytest
from services.__main__ import init_app
from multidict import MultiDictProxy, MultiDict


@pytest.fixture
async def cli(aiohttp_client):
    app = await init_app()
    return await aiohttp_client(app)


async def test_index(cli):
    response = await cli.get("/dishes")
    assert response.status == 200


async def test_create(cli):
    dish = {"name": "Дуб"}
    data = MultiDictProxy(MultiDict(dish.items()))
    response = await cli.post("/dishes", data=data)
    assert response.status == 200


async def test_available(cli):
    response = await cli.get("/dishes/1")
    assert response.status == 200


async def test_duplicate(cli):
    dish = {"name": "Дуб"}
    data = MultiDictProxy(MultiDict(dish.items()))
    response = await cli.post("/dishes", data=data)
    assert response.status == 400

