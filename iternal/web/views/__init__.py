from aiohttp import web

from .base import index


def route(app: web.Application) -> None:
    add_route = app.router.add_route
    add_route("POST", index, name="app.index")
