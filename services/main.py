from aiohttp import web
import jinja2
import aiohttp_jinja2
import logging
from dishes.routes import setup_routes
from dishes.db import init_db, create_tables
from dishes.middlewares import handle_error
from aiohttp.web_middlewares import normalize_path_middleware
from settings import APP_HOST, APP_PORT
import sys
import asyncio

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


async def init_app():
    app = web.Application(middlewares=[
        normalize_path_middleware(append_slash=False, remove_slash=True),
        handle_error
    ])
    setup_routes(app)

    aiohttp_jinja2.setup(
        app, loader=jinja2.PackageLoader('dishes')
    )
    await init_db(app)
    create_tables()
    return app


def main():
    logging.basicConfig(level=logging.DEBUG)
    app = init_app()
    web.run_app(app, host=APP_HOST, port=APP_PORT)


if __name__ == '__main__':
    main()
