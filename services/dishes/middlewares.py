from aiohttp import web


@web.middleware
def cut_slash(request, handler):
    pass