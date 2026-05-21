from __future__ import annotations

from core.fetch.http_fetcher import fetch_sync, fetch_async


def fetch_markdown_sync(url: str):
    data = fetch_sync(url)
    data["source"] = "markdown"
    return data


async def fetch_markdown_async(url: str):
    data = await fetch_async(url)
    data["source"] = "markdown"
    return data

