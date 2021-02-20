import aiohttp_jinja2
from aiohttp import web
import jinja2
from typing import Union, List
from pathlib import Path

from .consts import APP_KEY
from .utils import gather_template_folders

# based on https://github.com/aio-libs/aiohttp_admin/ or copy'n past
__all__ = (
    "setup",
)


def setup(
    app: web.Application,
    prefix: str,
    *,
    static_folder: Path = None,
    template_folder: Union[Path, List[Path]] = None,
    app_key: str = APP_KEY
) -> None:
    admin_app = web.Application()
    app[app_key] = admin_app

    templatef = gather_template_folders(template_folder)
    loader = jinja2.FileSystemLoader(templatef)
    aiohttp_jinja2.setup(admin_app, loader=loader, app_key=app_key)
