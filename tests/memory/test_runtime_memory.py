from core.memory import run_runtime_memory


def test_memory_determinism():
    sources = {
        "workflow": {"objective": "monitor_metrics"},
        "semantic": {"semantic": {"domain": {"domain": "analytics"}}},
    }

    first = run_runtime_memory(sources=sources, tick=1)
    second = run_runtime_memory(sources=sources, tick=1)

    assert first["runtime"] == second["runtime"]
    assert first["graph"] == second["graph"]
    assert first["index"] == second["index"]
