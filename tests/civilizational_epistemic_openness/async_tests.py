import asyncio

from core.evidence import structure_cognition


def test_async_structure_cognition():
    async def run():
        return structure_cognition({"a": 1}, {"b": 2}, {"a": 1})

    r = asyncio.run(run())
    assert r["civilizational_openness"]["open"] is True
