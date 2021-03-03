from __future__ import annotations

import asyncio
import logging
from pathlib import Path

from aiohttp import web
from aiohttp_jinja2 import render_template
from aiohttp_security import remember, forget
from yarl import URL
from typing import Union, Optional

from .consts import APP_KEY, TEMPLATE_APP_KEY
from .security import authorize
from .utils import validate_payload, json_response, LoginForm
from .exceptions import JsonValidationError

__all__ = (
    "AdminHandler",
    "setup_admin_handlers"
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
        if template is not None:
            assert template.endswith(".html") or template.endswith(".jinja2"), "Template Name should endswith .html or .jinja2"

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

    async def login_page(self, request: web.Request):
        t = self._login_template
        return render_template(t, request, {}, app_key=TEMPLATE_APP_KEY)

    async def token(self, request: web.Request):
        raw_payload = await request.read()
        data: dict = validate_payload(raw_payload, LoginForm)
        await authorize(request, data['username'], data['password'])

        router = request.app.router
        location = router["admin.index"].url_for().human_repr()
        payload = {"location": location}
        response = json_response(payload)
        await remember(request, response, data['username'])
        return response

    async def logout(self, request: web.Request):
        if "Authorization" not in request.headers:
            msg = "Auth header is not present, can not destroy token"
            raise JsonValidationError(msg)
        router = request.app.router
        location = router["admin.login"].url_for().human_repr()
        payload = {"location": location}
        response = json_response(payload)
        await forget(request, response)
        return response


def setup_admin_handlers(
    app: web.Application,
    handler: AdminHandler,
    static_folder: Union[str, Optional[Path]],
    prefix: str = None,
) -> None:
    if prefix is None:
        prefix = '/admin'

    logger.debug("setuping admin handlers...")

    add_route = app.router.add_route

    add_route("GET", "/", handler.index_page, name=f"admin.index")
    app.router.add_static(prefix, static_folder, name=f"admin.static")


class AdminHandlerRest:
    pass
