from pathlib import Path
from typing import Union, List

import trafaret as t

from iternal.web.admin.consts import TEMPLATES_ROOT
from .exceptions import JsonValidationError


try:
    import ujson as json
except ImportError or ModuleNotFoundError:
    import json

__all__ = "gather_template_folders", "validate_payload"


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


def validate_payload(raw_payload, schema):
    payload = raw_payload.decode(encoding='UTF-8')
    try:
        parsed = json.loads(payload)
    except ValueError:
        raise JsonValidationError('Payload is not json serialisable')

    try:
        data = schema(parsed)
    except t.DataError as exc:
        raise JsonValidationError(**as_dict(exc))
    return data


def as_dict(exc, value=None):
    result = exc.as_dict(value)
    if isinstance(result, str):
        return {"error": result}
    return result
