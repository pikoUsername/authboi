from __future__ import annotations

import sys

import asyncio
from aiohttp import web


class AdminHandler(web.View):
    __slots__ = "app", "loop", "resources", "name"

    def __init__(
        self,
        app: web.Application,
        loop: asyncio.AbstractEventLoop = None,
        *, resources=None,
        name: str = None
    ) -> None:
        self.app = app
        self.loop = loop
        self.resources = resources
        self.name = name


def setup_admin_handler(app: web.Application, handler)
