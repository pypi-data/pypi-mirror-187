"""Module with JSON template creation and request data validation."""

import json
from functools import wraps

import aiohttp.web
import aiohttp.web_request
from pydantic import BaseModel

from aiojsonapi.exception import ApiException, DataMissing, UnknownFields
from aiojsonapi.request import Request
from aiojsonapi.response import BadResponse, GoodResponse


class JSONTemplate:
    """Structure based on pydantic model."""

    def __init__(self, template: type[BaseModel] = None, ignore_unknown=True):
        self.template = template
        self.ignore_unknown = ignore_unknown

    def __call__(self, func):
        @wraps(func)
        async def wrap(*args, **kwargs):
            try:
                request = None
                for arg in args:
                    if isinstance(arg, aiohttp.web_request.Request):
                        request = arg
                if await request.read():
                    request = Request(await request.json())
                try:
                    request.validated_data = self.template(**request.data)
                except TypeError as error:  # kinda hacky :(
                    error = str(error)
                    path = error.split("'")[1]
                    if "missing" in error:
                        raise DataMissing(path) from None
                    raise UnknownFields(path) from None
                result = await func(request, **kwargs)
                if isinstance(result, aiohttp.web.StreamResponse):
                    return result
                return GoodResponse(result)
            except ApiException as error:
                return BadResponse(error.message, status=error.status)
            except json.decoder.JSONDecodeError:
                return BadResponse("Wrong json data format")
            except BaseException as error:
                return BadResponse(repr(error))

        return wrap
