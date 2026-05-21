from __future__ import annotations

from core.fetch.http_fetcher import fetch_sync, fetch_async


def fetch_medium_sync(url: str):
    data = fetch_sync(url)
    data["source"] = "medium"
    return data


async def fetch_medium_async(url: str):
    data = await fetch_async(url)
    data["source"] = "medium"
    return data

