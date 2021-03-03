import asyncio
from typing import Optional

import aiohttp
from loguru import logger
try:
    import ujson as json
except ImportError:
    import json


async def make_request(
    session: aiohttp.ClientSession,
    method_http: str,
    method: str,
    data: dict,
    **kwargs
):
    assert method.startswith("/"), f"Method should endswith '/', instead of {method[0]}"
    logger.debug(f"Making Request: method: {method}, with data: {data}")

    url = "https://api.github.com/{method}"

    async with session.request(method_http, url.format(method=method_http), data=data, **kwargs) as r:
        return r.text()


class GithubWrap:
    """
    For log, and etc.
    """
    def __init__(
            self,
            loop: Optional[asyncio.AbstractEventLoop] = None,
            session: Optional[aiohttp.ClientSession] = None,
    ) -> None:
        self._loop = loop
        self._session = session

    def get_new_session(self) -> aiohttp.ClientSession:
        return aiohttp.ClientSession(
            loop=self.loop,
            json_serialize=json.dumps
        )

    @property
    def loop(self) -> Optional[asyncio.AbstractEventLoop]:
        if self.loop is None:
            self._loop = asyncio.get_event_loop()
        return self._loop

    @property
    def session(self):
        if self._session is None:
            self._session = self.get_new_session()
        return self._session

    async def send_request(self, http_method: str, method: str, data: dict, **kwargs):
        return await make_request(self.session, http_method, method, data, **kwargs)

    async def read_commits(self, owner: str, repo: str):
        # todo read commits

        return await self.send_request()
