import aiohttp_jinja2
from services.dishes import db
from services.dishes.middlewares import check
from aiohttp import web
import json


class IndexView(web.View):
    @aiohttp_jinja2.template("index.html")
    async def get(self):
        async with self.request.app["db"].acquire() as conn:
            dishes = await db.get_dishes(conn)
            return {"message": dishes}

    async def post(self):
        form = await self.request.json()
        async with self.request.app["db"].acquire() as conn:
            form = dict(form)
            new_dish_id = await db.insert_dish(conn, form)
            return web.json_response({"message": str(new_dish_id)})


@aiohttp_jinja2.template("delegate.html")
class DelegateView(web.View):

    @check
    async def get(self):
        dish_id = self.request.match_info["dish_id"]
        async with self.request.app["db"].acquire() as conn:
            dishes = await db.get_single_dish(conn, dish_id)
            return {"message": dishes}

    async def post(self):
        pass

    async def delete(self):
        dish_id = int(self.request.path.split("/")[-1])
        async with self.request.app["db"].acquire() as conn:
            await db.delete_dish(conn, dish_id)

    async def update(self):
        pass
