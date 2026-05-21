import asyncio

import webweavex as ww


def test_async():
    assert isinstance(asyncio.run(ww.extract_async("# T")), dict)
