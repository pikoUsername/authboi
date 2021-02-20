from __future__ import annotations

import asyncio
import logging

from aiohttp import web
from yarl import URL
from aiohttp_jinja2 import render_template
from aiohttp_security import remember, forget

from .consts import APP_KEY, TEMPLATE_APP_KEY
from .utils import validate_payload
from .exceptions import JsonValidationError

__all__ = (
    "AdminHandler",
    "setup_admin_handler"
)

logger = logging.getLogger(APP_KEY)


class AdminHandler:
    """
    Main Admin Handler.
    Lower in Code, have rest twin
    """
    # using "private" settings, bc user may change this consts
    # its python, so all can be possible
    __slots__ = [
        "_admin",
        "_loop",
        "_name",
        "_template",
        "_login_template",
        "_resources"
    ]

    def __init__(
        self,
        admin: web.Application,
        loop: asyncio.AbstractEventLoop = None,
        *, resources=None,
        name: str = None,
        template: str = None
    ) -> None:
        assert template.endswith(".html"), "Template Name should endswith .html"

        self._admin = admin
        self._loop = loop if loop else asyncio.get_event_loop()
        self._name = name or 'admin'
        self._template = template or 'admin.html'
        self._login_template = 'login.html'

        for r in resources:
            r.setup(self._admin, URL('/'))
        self._resources = tuple(resources)

    # =========================
    # properties
    # =========================

    @property
    def template(self) -> str:
        return self._template

    @template.setter
    def template(self, _) -> None:
        import warnings

        warnings.warn("Template property is RO")

    @property
    def name(self):
        return self._name

    @property
    def resources(self):
        return self._resources

    # =========================
    # views for admin page
    # =========================

    async def index_page(self, request: web.Request):
        t = self._template
        context = {'name': self._name}
        return render_template(t, request, context, app_key=TEMPLATE_APP_KEY)

    async def login_page(self, request):
        t = self._login_template
        return render_template(t, request, {}, app_key=TEMPLATE_APP_KEY)

    async def token(self, request):
        raw_payload = await request.read()
        data = validate_payload(raw_payload, LoginForm)
        await authorize(request, data['username'], data['password'])

        router = request.app.router
        location = router["admin.index"].url_for().human_repr()
        payload = {"location": location}
        response = json_response(payload)
        await remember(request, response, data['username'])
        return response

    async def logout(self, request):
        if "Authorization" not in request.headers:
            msg = "Auth header is not present, can not destroy token"
            raise JsonValidationError(msg)
        router = request.app.router
        location = router["admin.login"].url_for().human_repr()
        payload = {"location": location}
        response = json_response(payload)
        await forget(request, response)
        return response


def setup_admin_handler(app: web.Application, handler: AdminHandler) -> None:
    logger.debug("setuping admin handlers...")

    add_route = app.router.add_route
    add_route("GET", "", handler.index_page, name="admin.index")
