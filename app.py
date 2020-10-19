
from aiohttp import web


def init(app):
    from src.handlers.User import dp




if __name__ == '__main__':
    web.run_app(init)