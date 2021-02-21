import asyncio
import aiohttp_jinja2
from aiohttp import web
import jinja2
from typing import Union, List, Any
from pathlib import Path

from .consts import APP_KEY, PROJ_ROOT
from .handler import AdminHandler, setup_admin_handlers
from .utils import gather_template_folders

# based on https://github.com/aio-libs/aiohttp_admin/ or copy'n past
__all__ = (
    "setup",
    "get_admin"
)


def setup(
    app: web.Application,
    prefix: str,
    *,
    static_folder: Path = None,
    template_folder: Union[Path, List[Path]] = None,
    app_key: str = APP_KEY,
    resources: Any = None,
    template_name: str = None,
    name: str = None,
    loop: asyncio.AbstractEventLoop = None,
) -> web.Application:
    loop = loop or asyncio.get_event_loop()
    admin = web.Application()  # need to test
    app[app_key] = admin

    template_folder = template_folder or Path(__file__).parent
    templatef = gather_template_folders(template_folder)
    loader = jinja2.FileSystemLoader(templatef)
    aiohttp_jinja2.setup(admin, loader=loader, app_key=app_key)

    template_name = template_name if template_name else "admin.html"
    resources = resources if resources else tuple()
    admin_handler = AdminHandler(admin, resources=resources, name=name,
                                 template=template_name, loop=loop)

    admin['admin_handler'] = admin_handler
    admin['layout_path'] = prefix

    static_folder = static_folder or str(PROJ_ROOT / 'static')
    setup_admin_handlers(admin, admin_handler, static_folder, prefix)
    return admin


def get_admin(app: web.Application, *, app_key=APP_KEY):
    return app.get(app_key, None)
