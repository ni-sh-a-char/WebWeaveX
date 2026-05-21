from __future__ import annotations

from typing import Dict

from core.fetch.http_fetcher import fetch_sync, fetch_async


def fetch_github_sync(url: str) -> Dict[str, object]:
    data = fetch_sync(url)
    data["source"] = "github"
    return data


async def fetch_github_async(url: str) -> Dict[str, object]:
    data = await fetch_async(url)
    data["source"] = "github"
    return data

