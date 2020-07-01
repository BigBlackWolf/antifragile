import aiohttp_jinja2
from services.dishes import db


@aiohttp_jinja2.template("index.html")
async def index(request):
    if request.method == "POST":
        form = await request.post()
        async with request.app["db"].acquire() as conn:
            form = dict(form)
            await db.insert_dish(conn, form)
            dishes = await db.get_dishes(conn)
            return {"message": dishes}
    else:
        async with request.app["db"].acquire() as conn:
            dishes = await db.get_dishes(conn)
            return {"message": dishes}
        

@aiohttp_jinja2.template("delegate.html")
async def delegate(request):
    dish_id = request.match_info["dish_id"]
    async with request.app["db"].acquire() as conn:
        dishes = await db.get_single_dish(conn, dish_id)
        return {"message": dishes}
