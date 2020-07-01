from aiopg.sa import create_engine
from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Table,
    DateTime, ForeignKey, MetaData, create_engine as cr
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
    Column("add_timestamp", DateTime, nullable=False, default=datetime.utcnow),
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


# async def get_dishes(conn):
#     j = dishes.join(recipes, dishes.c.id == recipes.c.dish_id)
#     records = await conn.execute(
#         select([dishes.c.name, recipes.c.id]).select_from(j)
#     )
#     fetched = await records.fetchall()
#     result = list(map(lambda x: {"Блюдо": x[0], "Id": x[1]}, fetched))
#     return result

async def get_dishes(conn):
    records = await conn.execute(
        dishes.select().order_by(dishes.c.add_timestamp)
    )
    fetched = await records.fetchall()
    result = list(map(lambda x: {"name": x[1], "id": x[0]}, fetched))
    return result


async def insert_dish(conn, data: dict):
    await conn.execute(
        dishes.insert().values(**data)
    )


async def get_single_dish(conn, dish_id):
    records = await conn.execute(
        dishes.select().where(dishes.c.id == dish_id)
    )
    fetched = await records.fetchall()
    result = list(map(lambda x: {"name": x[1], "id": x[0]}, fetched))
    return result
