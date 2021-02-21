import asyncio
from aiohttp import web
from iternal.web import admin


def test_get_admin():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    app = web.Application()

    admin_app = admin.setup(app, "./chernobill", resources=tuple())

    result = admin.get_admin(app)
    assert admin_app is result, "admin_app must be same when get_admin method"


def test_setup_admin():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    app = web.Application()

    admin_app = admin.setup(app, "/HAHAHAHA", resources=tuple())

    assert app[admin.APP_KEY] is admin_app, "oh no"


def test_get_admin_other_key():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    app = web.Application()
    app_key = "yoyoyo"

    admin_app = admin.setup(app, "dsds", resources=tuple(), app_key=app_key)

    other = admin.get_admin(app, app_key=app_key)

    assert admin_app is other
