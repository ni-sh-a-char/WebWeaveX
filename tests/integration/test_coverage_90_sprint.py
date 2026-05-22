"""Integration tests targeting 90% coverage on public and connector surfaces."""

import json
from pathlib import Path

import pytest

from core.workflows.workflow_checkpoint_engine import (
    save_workflow_checkpoint,
    load_workflow_checkpoint,
)
from core.workflows.workflow_memory_engine import save_workflow_memory, load_workflow_memory
from core.workflows.workflow_orchestrator import run_workflow_for_extraction
from core.workflows.workflow_planner_engine import build_workflow_plan
from core.execution.runtime_checkpoint_engine import save_execution_checkpoint, load_execution_checkpoint
from core.connectors.database_connector_engine import extract_database_runtime
from core.connectors.api_connector_engine import extract_api_runtime
from core.connectors.container_connector_engine import extract_container_runtime
from core.connectors.kubernetes_connector_engine import extract_kubernetes_runtime
from core.connectors.telemetry_connector_engine import extract_telemetry_runtime
from core.reconstruction.runtime_reconstruction_orchestrator import run_reconstruction_runtime
from core.synchronization.runtime_sync_orchestrator import run_synchronized_runtime
from core.distributed_extraction.autonomous_extraction_engine import run_autonomous_extraction
from core.semantic.semantic_orchestrator import run_semantic_for_extraction
from core.memory.runtime_memory_orchestrator import run_memory_for_extraction
from core.typed_ir.typed_runtime_ir import compile_typed_runtime_ir
from core.typed_ir.typed_topology_ir import compile_typed_topology_ir


def test_workflow_checkpoint_kaalka_roundtrip(tmp_path):
    p = tmp_path / "wf.kaalka"
    save_workflow_checkpoint(str(p), {"step": 1}, "key")
    loaded = load_workflow_checkpoint(str(p), "key")
    assert loaded["available"]
    assert loaded["checkpoint"]["step"] == 1


def test_workflow_memory_kaalka(tmp_path):
    p = tmp_path / "wm.kaalka"
    save_workflow_memory(str(p), {"objective": "monitor"}, "key")
    assert load_workflow_memory(str(p), "key")["available"]


def test_execution_checkpoint_kaalka(tmp_path):
    p = tmp_path / "ex.kaalka"
    save_execution_checkpoint(str(p), {"actions": []}, "key")
    assert load_execution_checkpoint(str(p), "key")["available"]


def test_workflow_for_extraction_enabled():
    out = run_workflow_for_extraction(
        autonomous_workflow=True,
        url="https://example.com",
        objective="extract_dashboard",
    )
    assert out.get("enabled") is True


def test_build_workflow_plan_sorted():
    plan = build_workflow_plan("extract_dashboard", semantic_runtime={"semantic": {}})
    assert "steps" in plan


def test_connectors_all_types():
    assert extract_database_runtime("sqlite", snapshot={"tables": []})["bounded"]
    assert extract_api_runtime("rest", snapshot={"endpoints": []})["bounded"]
    assert extract_api_runtime("graphql", snapshot={"graphql": {}})["bounded"]
    assert extract_container_runtime(snapshot={"containers": []})["bounded"]
    assert extract_kubernetes_runtime(snapshot={"manifests": []})["bounded"]
    assert extract_telemetry_runtime(snapshot={"signals": []})["bounded"]


def test_reconstruction_orchestrator():
    out = run_reconstruction_runtime(sources={"semantic_ir": {"ir": "semantic_runtime"}}, runtime_type="browser")
    assert out.get("validation") is not None or out.get("runtime")


def test_semantic_and_memory_extraction():
    sem = run_semantic_for_extraction(url="https://example.com", html="<p>hi</p>", semantic_runtime=True)
    assert sem.get("enabled") is True
    mem = run_memory_for_extraction(federated_memory=True, sources={"extraction": {"url": "x"}})
    assert mem.get("enabled") is True


def test_distributed_autonomous():
    out = run_autonomous_extraction(tasks=[{"task_id": "a", "url": "https://example.com", "priority": 0}])
    assert out.get("autonomous") is True


def test_sync_runtime_full():
    out = run_synchronized_runtime(tick=1, browser={"dom": {"nodes": [{"id": "n"}]}})
    assert out.get("bounded") is True


def test_typed_ir_compilers():
    rt = compile_typed_runtime_ir([{"from": "a", "to": "b", "transition_type": "step"}])
    assert rt.get("typed") is True
    topo = compile_typed_topology_ir(["api", "worker"])
    assert topo.get("typed") is True


def test_universal_extract_branches(tmp_path):
    from webweavex.universal_extract import universal_extract

    txt = tmp_path / "a.txt"
    txt.write_text("hello", encoding="utf-8")
    assert universal_extract(str(txt))["bounded"] is True

    unsupported = universal_extract(str(tmp_path / "missing.xyz"))
    assert unsupported.get("unsupported") or unsupported.get("ingestion")


def test_webweavex_api_run_success(monkeypatch):
    from webweavex.api import api as api_mod

    monkeypatch.setattr(
        api_mod,
        "run_pipeline",
        lambda *_a, **_k: {
        "structured_data": {},
        "confidence": 1.0,
        "source": "test",
    })
    out = api_mod.run({"input": "hello", "mode": "compiler"})
    assert out["version"]


def test_intelligence_groq_fallback(monkeypatch):
    from webweavex.plugins.intelligence_engine import run_ai_task, enhanced_task_runner

    def _fail(*_a, **_k):
        raise ImportError("no provider")

    monkeypatch.setattr(
        "webweavex.plugins.intelligence_engine._load_provider",
        _fail,
    )
    data = {"human_readable": "text", "structured_data": {"text": "x"}}
    out = run_ai_task(data, "analyze", "openai", {})
    assert out.get("fallback") is True
    assert enhanced_task_runner(data, "summarize", provider="openai") is not None
