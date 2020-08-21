from aiopg.sa import create_engine
from datetime import datetime
import sqlalchemy
from sqlalchemy import (
    Column, Integer, String, Table,
    DateTime, ForeignKey, MetaData, create_engine as cr,
    select
)
from settings import (
    DB_NAME, DB_HOST, DB_PASSWORD, DB_USERNAME
)
import logging

METADATA = MetaData()
DSN = "postgres://knooejhchvacqp:6243dcb6bed248fc29c3b45028c0a9ab571202f7c5978b1008132610aeaf51a4@ec2-54-247-78-30.eu-west-1.compute.amazonaws.com:5432/d3j96te1p86pgb"

dishes_ingredients = Table(
    'dishes_ingredients', METADATA,

    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("dish_id", Integer, ForeignKey("dishes.id", ondelete="CASCADE")),
    Column("ingredient_id", Integer, ForeignKey("ingredients.id", ondelete="CASCADE")),
    Column("quantity", Integer, default=1),
)

dishes_categories = Table(
    "dishes_categories", METADATA,

    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("dish_id", Integer, ForeignKey("dishes.id", ondelete="CASCADE")),
    Column("category_id", Integer, ForeignKey("categories.id", ondelete="CASCADE")),
)

dishes = Table(
    "dishes", METADATA,

    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(100), nullable=False, unique=True),
    Column("timestamp", DateTime, default=datetime.utcnow),
    Column("photo_url", String(255)),
    Column("recipe", String(1024)),
)

ingredients = Table(
    "ingredients", METADATA,

    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(100), unique=True),
)

categories = Table(
    "categories", METADATA,

    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(50), unique=True),
)


async def init_db(app):
    engine = await create_engine(dsn=DSN)
    app["db"] = engine


def create_tables():
    engine = cr(DSN)
    METADATA.create_all(engine)
    import os
    print(os.getcwd())
    with open("services/init.sql", 'r') as f:
        sql = sqlalchemy.text(f.read())
    try:
        engine.execute(sql)
    except Exception as e:
        print("Already created")


async def get_dishes(conn) -> list:
    try:
        records = await conn.execute(
            dishes.select().order_by(dishes.c.timestamp)
        )
    except Exception as e:
        logging.error("ERROR >>>>>> {}".format(e))
        return []
    fetched = await records.fetchall()
    result = list(map(lambda x: {"name": x[1], "id": x[0]}, fetched))
    return result


async def get_categories(conn) -> list:
    try:
        result = await conn.execute(
            select([categories.c.id, categories.c.name]).order_by(categories.c.name)
        )
    except Exception as e:
        logging.error("ERROR >>>>>> {}".format(e))
        return []
    else:
        result = await result.fetchall()
        return [{"name": i[1], "id": i[0]} for i in result]


async def get_ingredients(conn) -> list:
    try:
        result = await conn.execute(
            select([ingredients.c.id, ingredients.c.name]).order_by(ingredients.c.name)
        )
    except Exception as e:
        logging.error("ERROR >>>>>> {}".format(e))
        return []
    else:
        result = await result.fetchall()
        return [{"name": i[1], "id": i[0]} for i in result]


async def insert_dish(conn, data: dict) -> int:
    category = data.pop("category", "")
    ingredients = data.pop("ingredients", "")
    try:
        result = await conn.execute(
            dishes.insert().values(**data).returning(dishes.c.id)
        )
        inserted_id = await result.fetchone()
        dish_id = inserted_id[0]
        await conn.execute(
            dishes_categories.insert().values(dish_id=dish_id, category_id=category)
        )
        await conn.execute(
            dishes_ingredients.insert().values([
                {
                    "dish_id": dish_id,
                    "ingredient_id": ingredient[0],
                    "quantity": ingredient[1]
                } for ingredient in ingredients
            ])
        )
    except Exception as e:
        logging.error("ERROR >>>>>> {}".format(e))
    else:
        return dish_id


async def insert_categories(conn, categories_list: list, ingredients_list: list):
    try:
        await conn.execute(
            categories.insert().values(*categories_list)
        )
        await conn.execute(
            ingredients.insert().values(*ingredients_list)
        )
    except Exception as e:
        logging.error("ERROR >>>>>> {}".format(e))
    else:
        print("Inserted categories")


async def get_single_dish(conn, dish_id: str) -> list:
    try:
        records = await conn.execute(
            dishes.select().where(dishes.c.id == dish_id)
        )
    except Exception as e:
        logging.error("ERROR >>>>>> {}".format(e))
        return []
    fetched = await records.fetchall()
    try:
        ingrs = await conn.execute(
            select([dishes.c.id, ingredients.c.name,
                    dishes_ingredients.c.quantity
                    ]).select_from(dishes_ingredients
                                   .join(dishes)
                                   .join(ingredients)
                                   ).where(dishes.c.id == dish_id))
    except Exception as e:
        logging.error("ERROR >>>>>> {}".format(e))
        return []
    ingrs_fetched = await ingrs.fetchall()
    ing = {}
    for i in ingrs_fetched:
        print(i)
        dish_id, ingr, quantity = i[0], i[1], i[2]
        if ing.get(dish_id, None):
            ing[dish_id].append({"name": ingr, "quantity": quantity})
        else:
            ing[dish_id] = [{"name": ingr, "quantity": quantity}]

    result = list(map(lambda x: {"id": x[0], "name": x[1], "timestamp": x[2],
                                 "photo_url": x[3], "recipe": x[4]}, fetched))
    if ing:
        for i in result:
            i["ingredients"] = ing[i["id"]]
    return result


async def delete_dish(conn, dish_id: str):
    try:
        await conn.execute(
            dishes.delete().where(dishes.c.id == dish_id)
        )
    except Exception as e:
        logging.error("ERROR >>>>>> {}".format(e))


async def update_dish_details(conn, data: dict):
    dish_id = data.pop("dish_id", -1)

    transaction = await conn.begin()
    try:
        await conn.execute(
            dishes.update()
                .where(dishes.c.id == dish_id)
                .values(**data)
        )
    except Exception as e:
        logging.error("ERROR >>>>>> {}".format(e))
        await transaction.rollback()
        return "FAIL"
    else:
        await transaction.commit()
        return "SUCCESS"


async def update_dish_ingredients(conn, data: dict):
    dish_id = data.pop("dish_id", -1)
    ingredients_data = data.get("ingredients", [])

    transaction = await conn.begin()
    try:
        for ingredient in ingredients_data:
            await conn.execute(
                dishes_ingredients.update()
                    .where(dishes_ingredients.c.dish_id == dishes.c.id)
                    .where(dishes_ingredients.c.ingredient_id == ingredients.c.id)
                    .where(dishes.c.id == dish_id)
                    .where(ingredients.c.name == ingredient["ingredient"])
                    .values(dish_id=select([dishes.c.id]).where(dishes.c.id == dish_id),
                            quantity=ingredient["quantity"])
            )
    except Exception as e:
        logging.error("ERROR >>>>>> {}".format(e))
        await transaction.rollback()
        return "FAIL"
    else:
        await transaction.commit()
        return "SUCCESS"

