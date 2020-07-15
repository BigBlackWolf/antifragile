from aiopg.sa import create_engine
from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Table,
    DateTime, ForeignKey, MetaData, create_engine as cr,
    select
)
from services.dishes.settings import (
    DB_NAME, DB_HOST, DB_PASSWORD, DB_USERNAME
)

METADATA = MetaData()
DSN = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

dishes_ingredients = Table(
    'dishes_ingredients', METADATA,

    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("dish_id", Integer, ForeignKey("dishes.id")),
    Column("ingredient_id", Integer, ForeignKey("ingredients.id")),
    Column("quantity", Integer, default=1),
)

dishes_categories = Table(
    "dishes_categories", METADATA,

    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("dish_id", Integer, ForeignKey("dishes.id")),
    Column("category_id", Integer, ForeignKey("categories.id")),
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


async def get_dishes(conn):
    records = await conn.execute(
        dishes.select().order_by(dishes.c.timestamp)
    )
    fetched = await records.fetchall()
    result = list(map(lambda x: {"name": x[1], "id": x[0]}, fetched))
    return result


async def insert_dish(conn, data: dict) -> int:
    result = await conn.execute(
        dishes.insert().values(**data).returning(dishes.c.id)
    )
    inserted_id = await result.fetchone()
    return inserted_id[0]


async def get_single_dish(conn, dish_id):
    records = await conn.execute(
        dishes.select().where(dishes.c.id == dish_id)
    )
    fetched = await records.fetchall()
    ingrs = await conn.execute(
        select([dishes.c.id, ingredients.c.name,
                dishes_ingredients.c.quantity
                ]).select_from(dishes_ingredients
                               .join(dishes)
                               .join(ingredients)
                               ).where(dishes.c.id == dish_id))
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


async def delete_dish(conn, dish_id):
    await conn.execute(
        dishes.delete().where(dishes.c.id == dish_id)
    )


async def update_dish(conn, data: dict):
    dish_id = data.pop("dish_id", -1)
    await conn.execute(
        dishes.update()
            .where(dishes.c.id == dish_id)
            .values(**data)
    )


async def update_recipe(conn, data: dict):
    dish_id = data.pop("dish_id", -1)
    await conn.execute(
        dishes_ingredients.update()
            .where(dishes_ingredients.c.dish_id == dishes.c.id)
            .where(dishes_ingredients.c.ingredient_id == ingredients.c.id)
            .where(dishes.c.id == dish_id)
            .where(ingredients.c.name == data["ingredient"])
            .values(dish_id=select([dishes.c.id]).where(dishes.c.name == "Овсянка"))
    )
