from aiomysql.sa import create_engine
from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Table,
    DateTime, ForeignKey, MetaData, create_engine as cr
)
from sqlalchemy.sql import select
from sqlalchemy.orm import relationship
from services.dishes.settings import (
    DB_NAME, DB_HOST, DB_PORT, DB_PASSWORD, DB_USERNAME
)
from sqlalchemy.ext.declarative import declarative_base

metadata = MetaData()
Base = declarative_base(metadata=metadata)


class Recipes(Base):
    __tablename__ = 'recipes'

    id = Column(Integer, primary_key=True)
    dish_id = Column(Integer, ForeignKey("dishes.id"))
    ingredient_id = Column(Integer, ForeignKey("ingredients.id"))
    quantity = Column(Integer, default=1)
    dish = relationship("Dishes", back_populates="recipes")


class Dishes(Base):
    __tablename__ = "dishes"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    recipe = Column(Integer, ForeignKey("recipes.id"))
    add_timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)


ingredients = Table(
    "ingredients", metadata,

    Column("id", Integer, primary_key=True),
    Column("name", String(100), nullable=False, unique=True),
    mysql_charset="utf8"
)
# class Ingredients(Base):
#     __tablename__ = "ingredients"
#
#     id = Column(Integer, primary_key=True)
#     name = Column(String(100), nullable=False, unique=True)
#     dishes = relationship("Dishes", secondary='recipes', back_populates="ingredients")


async def init_db():
    # DSN = f"mysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_PORT}:{DB_PORT}/{DB_NAME}"
    pool = await create_engine(user=DB_USERNAME, password=DB_PASSWORD,
                               db=DB_NAME, host=DB_HOST, port=DB_PORT)
    return pool


def create_tables():
    DSN = f"mysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}?charset=utf8"
    engine = cr(DSN)
    metadata.create_all(engine)
    # conn = engine.connect()
    # res = conn.execute("SELECT * FROM ingredients")
    # for i in res:
    #     print(i)


create_tables()
