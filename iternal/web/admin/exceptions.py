"""
AdminRESTError:
    ObjectNotFound
    JsonValidationError
    Flood
"""
from __future__ import annotations

from typing import Any

from aiohttp import web

try:
    import ujson as json
except ImportError or ModuleNotFoundError:
    import json


class AdminRESTError(web.HTTPError):
    status_code = 500
    error = "Unknown Error"

    def __init__(self, message=None, status_code: int = None, **kwargs: Any):

        if status_code:
            self.status_code = status_code

        super().__init__(reason=message)
        if not message:
            message = self.error

        msg_dict = {"error": message}

        if kwargs:
            msg_dict['error_details'] = kwargs

        self.text = json.dumps(msg_dict)
        self.content_type = 'application/json'


class ObjectNotFound(AdminRESTError):
    status_code = 404
    error = "Object not found"


class JsonValidationError(AdminRESTError):
    status_code = 400
    error = "Invalid json payload"


class JsonForbiddenError(AdminRESTError):
    status_code = 403
    error = "Access denied"


class Flood(AdminRESTError):
    status_code = 420
    error = "Wait for {} second."

    def __init__(self, *args, wait_time: int, **kwargs):
        super(Flood, self).__init__(
            message=self.error.format(wait_time),
            *args,
            **kwargs
        )

        self.wait_time = wait_time
