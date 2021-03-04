import asyncio
from typing import Optional

import aiohttp
from loguru import logger

try:
    import ujson as json
except ImportError:
    import json

__all__ = "github_api",

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
        **kwargs
):
    assert method.startswith("/"), f"Method should endswith '/', instead of {method[0]}"
    logger.debug(f"Making Request: method: {method}, with data: {data}")

    url = "https://api.github.com/{method}"
    data = compose_data(data)

    async with session.request(
            method_http,
            url.format(method=method.format(**kwargs)),
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
            and not k.startswith('_') or not k.startswith("__")}


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

    async def read_commits(self, owner: str, repo: str, **kwargs):
        """
        Get Commits from github repo

        Can overhead, if commits dict huge.
        """
        return await self.send_request(
            "GET",
            "/repos/{owner}/{repo}",
            dict(**kwargs),
            owner=owner,
            repo=repo
        )

    async def read_comments_commit(self, owner: str, repo: str, commit_sha: str, **kwargs):
        """
        Gets comments for commit
        """
        data = generate_payload(**locals(), exclude=['owner', 'repo', 'commit_sha'])

        return await self.send_request(
            "GET", "/repos/{owner}/{repo}/{commit_sha}/comments",
            data=data,
            repo=repo,
            owner=owner,
            commit_sha=commit_sha
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


github_api = GithubWrap()
