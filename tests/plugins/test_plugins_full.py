"""Cover webweavex plugin registry and task runners."""

import pytest

from webweavex.plugins import (
    Plugin,
    execute_plugins,
    register_plugin,
    task_summarize,
    task_explain,
    task_analyze,
    run_task,
    build_graph,
    generate_actions,
    load_provider,
)
from webweavex.plugins.intelligence_engine import enhanced_task_runner


class _Boom(Plugin):
    name = "boom"

    def execute(self, data, config):
        raise RuntimeError("fail")


def test_plugin_tasks_and_fail_safe(monkeypatch):
    data = {"structured_data": {"text": "hello " * 50}, "confidence": 0.9}
    assert task_summarize(data)["summary"]
    assert task_explain(data)["explanation"]
    assert task_analyze(data)["analysis"]
    register_plugin("boom", _Boom())
    out = execute_plugins(data, ["boom"], {})
    assert out == data

    ai = enhanced_task_runner(data, "summarize", provider=None)
    assert ai

    assert run_task(data, "summarize")["summary"]
    assert run_task(data, "unknown")["error"]
    assert run_task(data, "summarize", provider="rule")["summary"]

    rich = {
        "structured_data": {
            "semantics": {
                "entities": [{"text": "User", "category": "noun"}],
                "actions": [{"text": "build", "category": "verb"}],
                "relationships": [{"from": "User", "to": "build", "type": "uses"}],
                "action_pairs": [{"normalized_action": "build", "entity": "api"}],
            },
            "reasoning": {"approach": ["install", "build", "run"], "strategy": "api"},
            "extra": "value",
        },
        "reconstructed_project": [{"path": "main.py", "content": "print(1)"}],
    }
    graph = build_graph(rich)
    assert graph["node_count"] >= 1
    actions = generate_actions(rich)
    assert len(actions) >= 3
    short = generate_actions({"structured_data": {}, "reconstructed_project": []})
    assert len(short) >= 3

    with pytest.raises(ValueError):
        load_provider("unknown")
    with pytest.raises(ImportError):
        load_provider("openai")

    monkeypatch.setattr(
        "webweavex.plugins.intelligence_engine.run_ai_task",
        lambda *a, **k: (_ for _ in ()).throw(RuntimeError("ai down")),
    )
    fallback = run_task(data, "summarize", provider="openai")
    assert fallback.get("summary")
