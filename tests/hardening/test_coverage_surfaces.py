"""Tests targeting previously low-coverage public surfaces."""

from core.contracts.graph_contracts import RuntimeGraphContract
from core.workflows.workflow_queue_engine import enqueue_workflow, dequeue_workflow


def test_runtime_graph_contract_sorts():
    g = RuntimeGraphContract.normalize(
        {
            "nodes": [{"id": "b"}, {"id": "a"}],
            "edges": [{"source": "z", "target": "a", "type": "x"}],
        }
    )
    assert g["nodes"][0]["id"] == "a"


def test_workflow_queue_roundtrip():
    enqueue_workflow({"id": "wf:1", "objective": "navigate", "priority": 0})
    item = dequeue_workflow()
    assert item["available"] is True
    assert item["workflow"]["objective"] == "navigate"


def test_webweavex_api_imports():
    import webweavex

    assert webweavex.__version__ == "2.0.0"
    assert callable(webweavex.extract_web)
    assert callable(webweavex.run_canonical_pipeline)


def test_plugins_registry():
    from webweavex.plugins import register_plugin, get_plugin, list_plugins, Plugin

    class _P(Plugin):
        name = "test_plugin"

    register_plugin("test_plugin", _P())
    assert "test_plugin" in list_plugins()
    assert get_plugin("test_plugin").name == "test_plugin"


def test_universal_extract_txt(tmp_path):
    from webweavex.universal_extract import universal_extract

    fp = tmp_path / "sample.txt"
    fp.write_text("hello webweavex", encoding="utf-8")
    out = universal_extract(str(fp))
    assert out.get("bounded") is True
