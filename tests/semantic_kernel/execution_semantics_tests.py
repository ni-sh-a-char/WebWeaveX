from core.repository.runtime_state_engine import model_runtime_state
from core.repository.async_execution_reasoner import reason_async_execution


def test_runtime_state_parser_backed():
    r = model_runtime_state("import os\n\ndef main():\n    pass\n", path="m.py")
    assert "evidence" in r
    assert len(r["transitions"]) >= 1


def test_async_reasoner():
    r = reason_async_execution("async def f():\n    await g()\n", path="a.py")
    assert "async" in r
