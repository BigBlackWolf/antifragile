import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import pytest
from main import init_app
import json


variables = {}


@pytest.fixture
async def cli(aiohttp_client):
    app = await init_app()
    return await aiohttp_client(app)


async def test_index(cli):
    response = await cli.get("/dishes")
    assert response.status == 200


async def test_create(cli):
    global variables
    dish = {"name": "Дуб"}
    data = json.dumps(dish)
    response = await cli.post("/dishes", data=data)
    res = await response.text()
    variables["dish_id"] = json.loads(res)["message"]
    assert response.status == 200


async def test_available(cli):
    global variables
    response = await cli.get("/dishes/{}".format(variables["dish_id"]))
    assert response.status == 200


async def test_duplicate(cli):
    dish = {"name": "Дуб"}
    data = json.dumps(dish)
    response = await cli.post("/dishes", data=data)
    assert response.status == 404


async def test_update_ingredients(cli):
    global variables
    dish = {"ingredients": [
        {"ingredient": "Помидор", "quantity": 10},
        {"ingredient": "Огурец", "quantity": 10},
        {"ingredient": "Картошка", "quantity": 10},
        {"ingredient": "Капуста", "quantity": 1}
    ]}
    data = json.dumps(dish)
    response = await cli.put("/dishes/{}".format(variables["dish_id"]), data=data)
    assert response.status == 200


async def test_update_recipe(cli):
    global variables
    dish = {"recipe": "New recipe"}
    data = json.dumps(dish)
    response = await cli.put("/dishes/{}".format(variables["dish_id"]), data=data)
    assert response.status == 200

    res = await response.text()
    app_status = json.loads(res)["message"]
    assert app_status == "SUCCESS"


async def test_error_page(cli):
    response = await cli.get("/dishes/asdasdasd")
    assert response.status == 404


async def test_negative_input(cli):
    content = {"reipe": "New recipe"}
    data = json.dumps(content)
    response = await cli.put("/dishes/".format(variables["dish_id"]), data=data)
    assert response.status == 404


async def test_delete(cli):
    global variables
    response = await cli.delete("/dishes/{}".format(variables["dish_id"]))
    assert response.status == 200
