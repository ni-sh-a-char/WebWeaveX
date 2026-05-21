from __future__ import annotations

from typing import Dict
import httpx
import requests

from core.fetch.base import FetchResponse

DEFAULT_TIMEOUT = 12.0
DEFAULT_RETRIES = 2
UA = "WebWeaveX/1.1 (+https://github.com/PIYUSH-MISHRA-00)"
DEFAULT_ACCEPT = "text/html,application/json,text/plain,application/xml;q=0.9,*/*;q=0.8"


def _response(source: str, url: str, status_code: int, content_type: str, text: str, error: str = "") -> Dict[str, object]:
    return FetchResponse(
        source=source,
        url=url,
        status_code=status_code,
        content_type=content_type or "text/plain",
        text=text or "",
        ok=(200 <= status_code < 400 and not error),
        error=error,
        metadata={"length": str(len(text or ""))},
    ).to_dict()


def fetch_sync(url: str, timeout: float = DEFAULT_TIMEOUT, retries: int = DEFAULT_RETRIES) -> Dict[str, object]:
    last_err = ""
    for _ in range(max(retries, 0) + 1):
        try:
            res = requests.get(
                url,
                timeout=timeout,
                headers={"User-Agent": UA, "Accept": DEFAULT_ACCEPT, "Accept-Encoding": "identity"},
                allow_redirects=True,
            )
            if res.status_code == 429:
                continue
            return _response("http", url, res.status_code, res.headers.get("content-type", ""), res.text)
        except Exception as exc:  # pragma: no cover
            last_err = str(exc)
    return _response("http", url, 0, "text/plain", "", last_err)


async def fetch_async(url: str, timeout: float = DEFAULT_TIMEOUT, retries: int = DEFAULT_RETRIES) -> Dict[str, object]:
    last_err = ""
    for _ in range(max(retries, 0) + 1):
        try:
            async with httpx.AsyncClient(
                timeout=timeout,
                headers={"User-Agent": UA, "Accept": DEFAULT_ACCEPT, "Accept-Encoding": "identity"},
                follow_redirects=True,
                limits=httpx.Limits(max_connections=20, max_keepalive_connections=10),
            ) as client:
                res = await client.get(url)
            if res.status_code == 429:
                continue
            return _response("http", url, res.status_code, res.headers.get("content-type", ""), res.text)
        except Exception as exc:  # pragma: no cover
            last_err = str(exc)
    return _response("http", url, 0, "text/plain", "", last_err)
