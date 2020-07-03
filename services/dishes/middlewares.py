from aiohttp import web
import functools
import aiohttp_jinja2


@web.middleware
async def handle_error(request, handler):
    try:
        return await handler(request)
    except Exception as e:
        return aiohttp_jinja2.render_template(
            "index.html", request, {"message": [{"id": 404, "name": "error"}]}, status=400
        )


def check(func):
    @functools.wraps(func)
    async def wrapper(request):
        print("custom middleware start")
        try:
            return await func(request)
        finally:
            print("custom middleware finished")
    return wrapper