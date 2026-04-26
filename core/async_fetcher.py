import aiohttp
import asyncio


async def fetch_async(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, timeout=10) as response:
            return await response.text()