import aiohttp_jinja2
from dishes import db
from dishes.middlewares import check
from aiohttp import web


class IndexView(web.View):
    @aiohttp_jinja2.template("index.html")
    async def get(self):
        async with self.request.app["db"].acquire() as conn:
            dishes = await db.get_dishes(conn)
            categories = await db.get_categories(conn)
            ingredients = await db.get_ingredients(conn)
        return {"message": dishes}


@aiohttp_jinja2.template("delegate.html")
class DelegateView(web.View):

    @check
    async def get(self):
        dish_id = self.request.match_info["dish_id"]
        async with self.request.app["db"].acquire() as conn:
            query = await db.get_single_dish(conn, dish_id)
            dish = query[0] if len(query) > 0 else {}
            return {"message": dish}

    async def delete(self):
        dish_id = int(self.request.path.split("/")[-1])
        async with self.request.app["db"].acquire() as conn:
            await db.delete_dish(conn, dish_id)
        return web.json_response({"message": "SUCCESS"})

    async def put(self):
        form = await self.request.json()
        form["dish_id"] = self.request.match_info["dish_id"]

        async with self.request.app["db"].acquire() as conn:
            if "ingredients" in form:
                new_dish_id = await db.update_dish_ingredients(conn, form)
            else:
                new_dish_id = await db.update_dish_details(conn, form)
        return web.json_response({"message": str(new_dish_id)})


@aiohttp_jinja2.template("submit-recipe.html")
class AddDishView(web.View):
    async def get(self):
        async with self.request.app["db"].acquire() as conn:
            categories = await db.get_categories(conn)
            ingredients = await db.get_ingredients(conn)
        return {"categories": categories, "ingredients": ingredients}

    async def post(self):
        form = await self.request.json()
        form = dict(form)
        async with self.request.app["db"].acquire() as conn:
            new_dish_id = await db.insert_dish(conn, form)
        return web.json_response({"message": str(new_dish_id)})


class SettingsView(web.View):
    @aiohttp_jinja2.template("settings.html")
    async def get(self):
        async with self.request.app["db"].acquire() as conn:
            categories = await db.get_categories(conn)
            ingredients = await db.get_ingredients(conn)
        return {"categories": categories, "ingredients": ingredients}

    async def post(self):
        form = await self.request.json()
        categories = form["categories"]
        ingredients = form["ingredients"]
        async with self.request.app["db"].acquire() as conn:
            await db.insert_categories(conn, categories)
            await db.insert_ingredients(conn, ingredients)
        return web.json_response({"message": "DONE"})
