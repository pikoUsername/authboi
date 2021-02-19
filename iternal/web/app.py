from aiohttp import web


def init_app() -> web.Application:
    # may use in cli/mng.py
    # and maybe this method have some issue
    # i dont know, yet
    app = web.Application()

    return app
