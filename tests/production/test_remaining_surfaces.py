"""Additional surface coverage for orchestrators and connectors."""

import pytest

from core.native.native_runtime_orchestrator import run_native_cognition
from core.distributed_extraction.autonomous_extraction_engine import (
    run_autonomous_extraction,
    save_distributed_checkpoint,
    load_distributed_checkpoint,
)
from core.intelligence.cluster_engine import detect_clusters
from core.graph.graph_reconstruction_engine import reconstruct_graph
from core.auth.authentication_runtime_engine import authenticate_runtime
from core.session.browser_session_snapshot_engine import capture_browser_session
from core.interaction.tab_runtime_engine import capture_tabs
from core.repository.kubernetes_semantic_engine import parse_kubernetes_semantics
from core.repository.service_boundary_engine import infer_service_boundaries
from core.evidence.evidence_graph_engine import build_evidence_graph
from core.ocr.ocr_engine import extract_ocr_text
from core.reconstruction.runtime_reconstruction_orchestrator import run_reconstruction_runtime
from webweavex.plugins.intelligence_engine import run_ai_task, build_prompt
from webweavex.universal_extract import universal_extract


def test_native_cognition():
    out = run_native_cognition(runtime="desktop", application="notepad", snapshot={"windows": []})
    assert out.get("bounded") is True


def test_autonomous_checkpoint_roundtrip(tmp_path):
    p = tmp_path / "d.kaalka"
    save_distributed_checkpoint(str(p), {"workers": [{"worker_id": "w0"}]}, "k")
    assert load_distributed_checkpoint(str(p), "k")["available"]


def test_autonomous_with_workers():
    out = run_autonomous_extraction(
        tasks=[{"task_id": "t1", "url": "https://a.test", "priority": 1}],
        workers=[{"worker_id": "w0", "capacity": 1}],
    )
    assert out.get("autonomous") is True


def test_cluster_and_graph():
    nodes = [{"id": "a"}, {"id": "b"}]
    edges = [{"from": "a", "to": "b"}]
    clusters = detect_clusters(nodes, edges)
    assert len(clusters) >= 1
    g = {"nodes": nodes, "edges": edges}
    assert reconstruct_graph(g).get("nodes")


def test_auth_and_session_snapshot():
    page = type("P", (), {"context": None})()
    assert authenticate_runtime(page, {}, {"method": "cookie_injection"}).get("bounded") is True
    ctx = type("C", (), {"cookies": lambda: []})()
    page = type("P", (), {"url": "https://x", "context": ctx})()
    snap = capture_browser_session(page, ctx)
    assert snap.get("bounded") is True


def test_tabs_and_repo_engines():
    ctx = type("C", (), {"_test_tabs": [{"index": 0, "url": "https://x"}]})()
    tabs = capture_tabs(ctx)
    assert tabs.get("tabs") is not None
    k8s = parse_kubernetes_semantics("apiVersion: v1\nkind: Pod\nmetadata:\n  name: web")
    assert k8s.get("workloads")
    bounds = infer_service_boundaries("service api {}\n")
    assert bounds.get("services") is not None or bounds.get("bounded") is True


def test_evidence_ocr_reconstruction():
    assert build_evidence_graph([{"id": "c1", "text": "fact"}]).get("nodes") is not None
    ocr = extract_ocr_text(__file__)
    assert "bounded" in ocr
    out = run_reconstruction_runtime(
        sources={"extraction": {"url": "x"}},
        runtime_type="browser",
        fabricate=True,
        clone=True,
    )
    assert out.get("bounded") is True or out.get("runtime") is not None


def test_intelligence_mock_and_prompts():
    data = {"human_readable": "hi", "structured_data": {"text": "hello world"}}
    assert build_prompt("summarize", data)
    mock = run_ai_task(data, "analyze", "mock", {})
    assert mock.get("success") is True


def test_universal_extract_pdf_branch(tmp_path, monkeypatch):
    pdf = tmp_path / "f.pdf"
    pdf.write_bytes(b"%PDF-1.4\n")
    monkeypatch.setattr(
        "core.ingestion.universal_ingestion_engine.ingest_input",
        lambda _p: {"input_type": "pdf", "bounded": True},
    )
    monkeypatch.setattr(
        "core.files.pdf_extraction_engine.extract_pdf_text",
        lambda _p: {"text": "pdf"},
    )
    out = universal_extract(str(pdf))
    assert out.get("bounded") is True
