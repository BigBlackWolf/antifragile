from aiohttp import web
from .views import index, DelegateView


def setup_routes(app):
    resources = [web.get("/dishes", index),
                 web.post("/dishes", index),
                 web.view(r"/dishes/{dish_id:\d+}", DelegateView),
                 ]
    app.add_routes(resources)
