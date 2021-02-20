from pathlib import Path
from typing import Union, List

from iternal.web.admin.consts import TEMPLATES_ROOT


def gather_template_folders(
        template_path: Union[Path, List[Path]]
) -> List[Path]:
    if not isinstance(template_path, list):
        template_path = [template_path]
    template_root = str(TEMPLATES_ROOT)
    if not template_path:
        template_folders = [template_root]
    else:
        template_folders = [template_root] + template_path
    return template_folders
