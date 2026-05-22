"""Autonomous extraction optional runtime branches."""

from core.distributed_extraction.autonomous_extraction_engine import run_autonomous_extraction


def test_autonomous_all_flags(tmp_path):
    cp = str(tmp_path / "cp.kaalka")
    out = run_autonomous_extraction(
        tasks=[{"task_id": "t1", "url": "https://example.com", "priority": 0}],
        workers=[{"worker_id": "w0"}],
        checkpoint_path=cp,
        checkpoint_key="k",
        objective_execution=True,
        native_extraction=True,
        causal_runtime=True,
        semantic_runtime=True,
        autonomous_workflow=True,
        workflow_federation=True,
        synchronized_runtime=True,
        evolving_runtime=True,
        federated_memory=True,
        execution_runtime=True,
        simulate_execution=True,
        reconstruction_runtime=True,
        fabricate_runtime=True,
        clone_runtime=True,
        evolution_memory_path=str(tmp_path / "e.kaalka"),
        federated_memory_path=str(tmp_path / "f.kaalka"),
        execution_memory_path=str(tmp_path / "x.kaalka"),
        reconstruction_memory_path=str(tmp_path / "r.kaalka"),
        evolution_memory_key="k",
        federated_memory_key="k",
        execution_memory_key="k",
        reconstruction_memory_key="k",
    )
    assert out.get("autonomous") is True
    assert out.get("bounded") is True
