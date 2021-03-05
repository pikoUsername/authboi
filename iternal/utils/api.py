import asyncio
from typing import Optional

import aiohttp
from loguru import logger

try:
    import ujson as json
except ImportError:
    import json

DEFAULT_FILTER = ['self', 'cls']


def compose_data(params: dict = None):
    data = aiohttp.FormData(quote_fields=False)

    if params is not None:
        for k, v in params.items():
            data.add_field(k, str(v))
    return data


async def make_request(
        session: aiohttp.ClientSession,
        method_http: str,
        method: str,
        data: dict,
        url_kw: dict = None,
        **kwargs
):
    assert method.startswith("/"), f"Method should endswith '/', instead of {method[0]}"
    logger.debug(f"Making Request: method: {method}, with data: {data}")

    url = f"https://api.github.com{method.format(**url_kw)}"
    data = compose_data(data)

    async with session.request(
            method_http,
            url,
            data=data,
            **kwargs
    ) as r:
        return await r.json()


def generate_payload(exclude: list = None, **kwargs):
    """
    Generate payload

    Usage: payload = generate_payload(**locals(), exclude=['foo'])

    :param exclude:
    :param kwargs:
    :return: dict
    """
    if exclude is None:
        exclude = []

    return {k: v for k, v in kwargs.items() if
            k not in exclude + DEFAULT_FILTER
            and v is not None
            and not k.startswith('_')
            or not k.startswith("__")}


class GithubWrap:
    """
    Github Api small support,
    idk how to make more comformatble
    """
    __slots__ = "loop", "_session", "_api_close_waiter"

    def __init__(
        self,
        loop: Optional[asyncio.AbstractEventLoop] = None,
        session: Optional[aiohttp.ClientSession] = None,
    ) -> None:
        self.loop = loop or asyncio.get_event_loop()
        self._session = session
        self._api_close_waiter = None

    @property
    def session(self):
        if self._session is None:
            self._session = aiohttp.ClientSession(loop=self.loop)
        return self._session

    async def send_request(self,
                           http_method: str,
                           method: str,
                           data: dict,
                           url_kwargs: dict = None,
                           **kwargs) -> dict:
        """
        Just Send request to github api
        """
        return await make_request(
            self.session,
            http_method,
            method,
            data,
            url_kwargs,
            **kwargs
        )

    async def read_commits(self, owner: str, repo: str, **kwargs):
        """
        Get Commits from github repo

        Can overhead, if commits dict huge.
        """
        data = generate_payload(**locals(), exclude=['owner', 'repo'])

        return await self.send_request(
            "GET",
            "/repos/{owner}/{repo}",
            data=data,
            url_kwargs={"owner": owner, "repo": repo}
        )

    async def read_comments_commit(self, owner: str, repo: str, commit_sha: str, **kwargs):
        """
        Gets comments for commit
        """
        data = generate_payload(**locals(), exclude=['owner', 'repo', 'commit_sha'])

        return await self.send_request(
            "GET", "/repos/{owner}/{repo}/{commit_sha}/comments",
            data=data,
            url_kwargs={'owner': owner, "repo": repo, "commit_sha": commit_sha}
        )

    async def issue(self, owner: str, repo: str, **kwargs):
        data = generate_payload(**locals(), exclude=['owner', 'repo'])
        return await self.send_request(
            "GET",
            "/repos/{owner}/{repo}/issue",
            data=data,
            owner=owner,
            repo=repo
        )

    def __del__(self):
        # looks like a bullshit
        self.loop.run_until_complete(self.session.close())
