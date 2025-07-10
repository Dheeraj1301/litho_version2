"""Minimal stub of the `httpx` library for local testing.
This implements the small subset used by `starlette.testclient`.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Mapping, Optional
from urllib.parse import urljoin, urlparse


class ByteStream:
    def __init__(self, data: bytes):
        self._data = data

    def read(self) -> bytes:
        return self._data


@dataclass
class URL:
    url: str

    def __post_init__(self):
        parsed = urlparse(self.url)
        self.scheme = parsed.scheme or "http"
        self.netloc = parsed.netloc.encode()
        self.path = parsed.path or "/"
        self.raw_path = self.path.encode()
        self.query = parsed.query.encode()

    def join(self, other: str | URL) -> "URL":
        return URL(urljoin(self.url, str(other)))

    def __str__(self) -> str:
        return self.url


class Request:
    def __init__(self, method: str, url: str | URL, headers: Optional[Mapping[str, str]] = None, content: bytes | None = None):
        self.method = method
        self.url = url if isinstance(url, URL) else URL(str(url))
        self.headers = dict(headers or {})
        self.content = content


class Response:
    def __init__(self, status_code: int = 200, headers: Optional[Mapping[str, str]] = None, content: bytes = b"", request: Request | None = None, stream: ByteStream | None = None):
        self.status_code = status_code
        self.headers = dict(headers or {})
        if stream is not None:
            content = stream.read()
        self.content = content
        self.request = request

    def json(self) -> Any:
        import json
        return json.loads(self.content.decode())

    @property
    def text(self) -> str:
        return self.content.decode()


class BaseTransport:
    def handle_request(self, request: Request) -> Response:
        raise NotImplementedError


class Client:
    def __init__(self, *, app: Any = None, base_url: str = "http://testserver", headers: Optional[Mapping[str, str]] = None, transport: Optional[BaseTransport] = None, follow_redirects: bool = True, cookies: Any = None):
        self.app = app
        self.base_url = URL(base_url)
        self.headers = dict(headers or {})
        self.transport = transport
        self.follow_redirects = follow_redirects
        self.cookies = cookies

    def request(self, method: str, url: str | URL, **kwargs: Any) -> Response:
        if not self.transport:
            raise RuntimeError("No transport provided")
        target = url if isinstance(url, URL) else self.base_url.join(str(url))
        headers = kwargs.get("headers", {})
        content = kwargs.get("content")
        req = Request(method, target, headers=headers, content=content)
        return self.transport.handle_request(req)

    def get(self, url: str | URL, **kwargs: Any) -> Response:
        return self.request("GET", url, **kwargs)


class UseClientDefault:
    """Placeholder for httpx's sentinel type."""
    pass


class _client:
    UseClientDefault = UseClientDefault
    USE_CLIENT_DEFAULT = UseClientDefault()
    CookieTypes = Any
    TimeoutTypes = Any
    AuthTypes = Any


class _types:
    URLTypes = str | URL
    RequestContent = Any
    RequestFiles = Any
    QueryParamTypes = Any
    HeaderTypes = Mapping[str, str]
    CookieTypes = Any
    AuthTypes = Any
    TimeoutTypes = Any
