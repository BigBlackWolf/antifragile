from aiohttp import web
from .views import index, delegate


def setup_routes(app):
    resources = [web.get("/dishes", index),
                 web.post("/dishes", index),
                 web.get(r"/dishes/{dish_id:\d+}", delegate)
                 ]
    app.add_routes(resources)
