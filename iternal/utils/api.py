import asyncio
from typing import Optional

import aiohttp
from loguru import logger

try:
    import ujson as json
except ImportError:
    import json

__all__ = "github_api",


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

    async with session.request(
            method_http,
            url.format(method=method.format(**kwargs)),
            data=data,
            **kwargs
    ) as r:
        return await r.json()


class GithubWrap:
    """
    Github Api small support,
    idk how to make more comformatble
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
        """
        Create Session if not exists, from get_new_session
        """
        if self._session is None:
            self._session = self.get_new_session()
        return self._session

    async def send_request(self,
                           http_method: str,
                           method: str,
                           data: dict,
                           **kwargs) -> dict:
        """
        Just Send request to github api
        """
        return await make_request(self.session, http_method, method, data, **kwargs)

    async def read_commits(self, owner: str, repo: str):
        """
        Get Commits from github repo

        Can overhead, if commits dict huge.
        """
        return await self.send_request("GET", "/repos/{owner}/{repo}", dict(), owner=owner, repo=repo)

    async def read_comments_commit(self, owner: str, repo: str, commit_sha: str):
        """
        Gets comments for commit
        """
        return await self.send_request(
            "GET", "/repos/{owner}/{repo}/{commit_sha}/comments",
            dict(), repo=repo, owner=owner, commit_sha=commit_sha
        )


github_api = GithubWrap()
