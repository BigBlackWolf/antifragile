from aiohttp import web
from .views import IndexView, DelegateView


def setup_routes(app):
    resources = [web.view(r"/dishes", IndexView),
                 web.view(r"/dishes/{dish_id:\d+}", DelegateView),
                 ]
    app.add_routes(resources)
