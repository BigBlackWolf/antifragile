from aiohttp import web
from .views import IndexView, DelegateView
import pathlib

ROOT_FOLDER = pathlib.Path(__file__).parent.parent


def setup_routes(app):
    resources = [web.view(r"/dishes", IndexView),
                 web.view(r"/dishes/{dish_id:\d+}", DelegateView),
                 web.static(r"/static/", str(ROOT_FOLDER) + '/dishes/resources')
                 ]
    app.add_routes(resources)
