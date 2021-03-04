import json
from functools import partial
from pathlib import Path
from typing import Union, List
from datetime import date, datetime

import trafaret as t
from aiohttp import web
try:
    from bson import ObjectId
except ImportError:
    ObjectId = None

from iternal.web.admin.consts import TEMPLATES_ROOT
from .exceptions import JsonValidationError


__all__ = (
    "gather_template_folders",
    "validate_payload",
    "as_dict",
    "jsonify",
    "json_datetime_serial",
    'json_response',
    "LoginForm"
)


LoginForm = t.Dict({
    "username": t.String,
    "password": t.String,
})


def gather_template_folders(
        template_path: Union[Path, List[Path]]
) -> List[str]:
    if not isinstance(template_path, list):
        template_path = [template_path]
    template_root = str(TEMPLATES_ROOT)
    if not template_path:
        template_folders = [template_root]
    else:
        template_folders = [template_root] + template_path
    return template_folders


def validate_payload(raw_payload: bytes, schema: t.Dict) -> Union[dict, list]:
    payload = raw_payload.decode(encoding='UTF-8')

    try:
        parsed = json.loads(payload)
    except ValueError:
        raise JsonValidationError('Payload is not json serializable')

    try:
        data = schema(parsed)
    except t.DataError as exc:
        raise JsonValidationError(**as_dict(exc))
    return data


def json_datetime_serial(
        obj: Union[ObjectId, datetime, date]
):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, (datetime, date)):
        serial = obj.isoformat()
        return serial

    if ObjectId is not None and isinstance(obj, ObjectId):
        return str(obj)

    raise TypeError("Object Not serialazible")


jsonify = partial(json.dumps, default=json_datetime_serial)

json_response = partial(web.json_response, dumps=jsonify)


def as_dict(exc, value=None):
    result = exc.as_dict(value)
    if isinstance(result, str):
        return {"error": result}
    return result
