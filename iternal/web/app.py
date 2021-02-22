from aiohttp import web
import aiohttp_jinja2
import jinja2

from iternal import config
from . import admin


def init_app() -> web.Application:
    app = web.Application()

    aiohttp_jinja2.setup(
        app, jinja2.FileSystemLoader(config.proj_path / "templates"))
    admin.setup(app, '/admins')  # todo working admin

    return app
