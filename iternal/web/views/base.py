import aiohttp_jinja2

from aiohttp import web


@aiohttp_jinja2.template('templates/app/index.html')
async def index(request: web.Request) -> None:
    return
