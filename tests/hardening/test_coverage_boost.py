from core.distributed_extraction.autonomous_extraction_engine import run_autonomous_extraction
from core.memory.runtime_merge_engine import merge_runtime_memories
from core.memory.runtime_memory_engine import build_runtime_memory
from core.synchronization.runtime_sync_orchestrator import run_synchronized_runtime
from core.execution.runtime_execution_orchestrator import run_execution_runtime
from core.runtime_graph.runtime_graph_engine import build_runtime_graph
from webweavex.api.schemas import validate_request
from webweavex.plugins import execute_plugins, register_plugin, Plugin, list_plugins


def test_validate_request_schema():
    req = validate_request({"input": "build api", "mode": "compiler"})
    assert req["input"] == "build api"


def test_execute_plugins_chain():
    class _Echo(Plugin):
        name = "echo"

        def execute(self, data, config):
            data = dict(data)
            data["echo"] = True
            return data

    register_plugin("echo", _Echo())
    out = execute_plugins({"x": 1}, ["echo"])
    assert out.get("echo") is True
    assert "echo" in list_plugins()


def test_memory_merge_deterministic():
    m1 = build_runtime_memory(runtime_history=[{"tick": 2, "kind": "sync"}])
    m2 = build_runtime_memory(runtime_history=[{"tick": 1, "kind": "workflow"}])
    merged = merge_runtime_memories([m2, m1])
    assert merged["stable_hash"]


def test_synchronization_runtime():
    out = run_synchronized_runtime(tick=0, browser={"dom": {"nodes": []}})
    assert out.get("bounded") is True


def test_execution_runtime_simulate():
    out = run_execution_runtime(runtime="browser", simulate=True)
    assert out.get("bounded") is True


def test_distributed_extraction_bounded():
    out = run_autonomous_extraction(
        tasks=[{"task_id": "t1", "url": "https://example.com", "priority": 0}],
        workers=[{"worker_id": "w0"}],
    )
    assert out.get("bounded") is True


def test_runtime_graph_merge():
    g = build_runtime_graph(
        [
            {"ir": "browser", "nodes": [{"id": "a"}], "edges": []},
            {"ir": "workflow", "nodes": [{"id": "b"}], "edges": []},
        ]
    )
    assert len(g.get("nodes", [])) >= 1
