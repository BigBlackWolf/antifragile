from aiohttp import web
from .views import index


def setup_routes(app):
    app.router.add_get('/dishes', index)
    app.router.add_post('/dishes', index)
