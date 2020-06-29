from aiohttp import web
import jinja2
import aiohttp_jinja2
import logging
from services.dishes.routes import setup_routes
from services.dishes.db import init_db, create_tables


async def init_app():
    app = web.Application()
    setup_routes(app)

    aiohttp_jinja2.setup(
        app, loader=jinja2.PackageLoader('services.dishes')
    )
    app["pool"] = await init_db()

    return app


def main():
    logging.basicConfig(level=logging.DEBUG)
    app = init_app()
    web.run_app(app)


if __name__ == '__main__':
    main()
