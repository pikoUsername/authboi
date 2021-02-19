from aiohttp import web
import aiohttp_jinja2
import jinja2

from iternal import config


def init_app() -> web.Application:
    # may use in cli/mng.py
    # and maybe this method have some issue
    # i dont know, yet
    app = web.Application()

    aiohttp_jinja2.setup(
        app, jinja2.FileSystemLoader(config.proj_path / ""))

    return app
