"""Broad integration tests for legacy V7 stack, checkpoints, and public API helpers."""

import json
from pathlib import Path

import pytest

import webweavex as wwx
from core.contracts.runtime_contracts import UniversalInput
from core.full_pipeline import run_pipeline
from core.intent_engine import resolve_intent
from core.source_orchestrator import build_source_plan
from core.query_builder import build_queries
from core.fetch_engine import fetch_all
from core.extraction_engine import BaseExtractor, extract_content, validate_extraction_engine
from core.ranking_engine import rank_results
from core.output_engine import build_output
from core.cache_engine import (
    generate_cache_key,
    save_cache,
    load_cache,
    clear_cache,
    should_cache,
    validate_cache_engine,
)
from core.kernel.runtime_pipeline import run_canonical_pipeline
from core.synchronization.runtime_checkpoint_engine import (
    save_runtime_sync_checkpoint,
    load_runtime_sync_checkpoint,
)
from core.semantic.semantic_checkpoint_engine import (
    save_semantic_checkpoint,
    load_semantic_checkpoint,
)
from core.causality.causal_checkpoint_engine import (
    save_causal_checkpoint,
    load_causal_checkpoint,
)
from core.evolution_runtime.runtime_evolution_checkpoint_engine import (
    save_evolution_checkpoint,
    load_evolution_checkpoint,
)
from core.schemas.validator import validate_contract
from webweavex.api.api import run as api_run


class _StubExtractor(BaseExtractor):
    def extract(self, url: str, html: str, metadata: dict):
        return {"url": url, "content": "ok"}


def test_legacy_v7_stack(tmp_path, monkeypatch):
    intent = resolve_intent("build calculator api")
    assert intent.get("type")

    plan = build_source_plan(intent)
    assert plan.get("sources") is not None

    queries = build_queries(intent, plan)
    assert "queries" in queries

    monkeypatch.setattr(
        "core.fetch_engine._safe_fetch",
        lambda url: "<html><body>x</body></html>",
    )
    fetched = fetch_all(queries)
    assert fetched.get("results") is not None

    ranked = rank_results(
        {
            "adaptive_results": [
                {
                    "query": "api",
                    "source": "web",
                    "base": {"text": "hello", "code": ["x = 1"]},
                    "recovered": {"recovered": [], "recovered_count": 0},
                }
            ]
        }
    )
    assert ranked.get("ranked_results")

    out = build_output(
        {
            "execution_type": "content",
            "result": ranked["ranked_results"][0].get("base", {}),
            "confidence": 0.8,
        },
        ranked["top_result"],
    )
    assert out.get("confidence") is not None

    key = generate_cache_key("probe")
    payload = {
        "human_readable": "x",
        "structured_data": {},
        "ui_schema": {},
        "confidence": 0.9,
        "source": "test",
        "reconstructed_project": [],
        "version": "v1",
    }
    assert should_cache(payload)
    save_cache(key, payload)
    assert load_cache(key) is not None
    clear_cache(key)
    assert validate_cache_engine()


def test_full_pipeline_branches():
    empty = run_pipeline("")
    assert empty["structured_data"]["spec"]["node_count"] == 0
    rich = run_pipeline("build-api, deploy_service")
    spec = rich["structured_data"]["spec"]
    assert spec["node_count"] >= 1
    assert spec["edge_count"] >= 0


def test_api_run_non_strict(monkeypatch):
    monkeypatch.setattr("webweavex.api.api.STRICT_CRE_DEFAULT", False)
    out = api_run({"input": "x", "mode": "compiler"})
    assert out.get("version")


def test_checkpoint_engines(tmp_path):
    key = "test-key"
    sync_p = tmp_path / "sync.kaalka"
    save_runtime_sync_checkpoint(str(sync_p), {"tick": 1}, key)
    assert load_runtime_sync_checkpoint(str(sync_p), key)["available"]

    sem_p = tmp_path / "sem.kaalka"
    save_semantic_checkpoint(str(sem_p), {"graph": {}}, key)
    assert load_semantic_checkpoint(str(sem_p), key)["available"]

    cau_p = tmp_path / "cau.kaalka"
    save_causal_checkpoint(str(cau_p), {"chain": []}, key)
    assert load_causal_checkpoint(str(cau_p), key)["available"]

    evo_p = tmp_path / "evo.kaalka"
    save_evolution_checkpoint(str(evo_p), {"generation": 0}, key)
    assert load_evolution_checkpoint(str(evo_p), key)["available"]


def test_canonical_pipeline_kinds(tmp_path):
    doc = tmp_path / "note.md"
    doc.write_text("# Title\n\nBody", encoding="utf-8")
    out = run_canonical_pipeline(
        UniversalInput(source=str(doc), path=str(doc), source_type="document"),
    )
    assert out.get("pipeline_hash")

    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "main.py").write_text("print(1)\n", encoding="utf-8")
    out2 = run_canonical_pipeline(
        UniversalInput(source=str(repo), path=str(repo), source_type="repository"),
    )
    assert out2.get("unified_runtime_graph") is not None


def test_schema_validator():
    graph = {"nodes": [{"id": "a", "kind": "node"}], "edges": [], "max_edges": 0}
    assert validate_contract(graph, "graph.schema.json") is True


def test_webweavex_public_helpers(monkeypatch):
    sample = {
        "relationships": {"execution_graph": {"nodes": [{"id": "a"}], "edges": []}},
        "content": {
            "repository": {"files": []},
            "documents": {"sections": []},
            "knowledge_v2": {},
            "knowledge_reconstruction_v18": {},
        },
    }
    assert wwx.query_graph(sample, node="a") is not None
    assert wwx.query_graph(graph={"nodes": [{"id": "b"}], "edges": []}, node="b") is not None
    assert wwx.query_graph() is not None
    assert wwx.query_repo(sample)
    assert wwx.query_knowledge(sample)
    assert wwx.query_knowledge(entities=[], edges=[])
    assert wwx.query_documents(text="hello")
    assert wwx.query_documents(sample)
    assert wwx.compile_document("doc")
    assert wwx.compile_repository("src", path=".")
    assert wwx.analyze([{"id": "a"}], [{"from": "a", "to": "a"}])

    monkeypatch.setattr(wwx, "_crawl", lambda url, **k: {"visited": [url], "discovered": []})
    monkeypatch.setattr(wwx, "extract", lambda url: {"relationships": {"execution_graph": {}}, "content": {}, "metadata": {}})
    assert wwx.extract_recursive("https://example.com")["metadata"]["crawl"]

    async def _crawl():
        return await wwx.crawl_async("https://example.com")

    import asyncio

    asyncio.run(_crawl())
    assert wwx.crawl("https://example.com")


def test_extraction_engine():
    assert validate_extraction_engine()
    out = extract_content("<html><body><pre>1</pre></body></html>")
    assert out["code"]


def test_stub_extractor():
    ex = _StubExtractor()
    assert ex.extract("https://example.com", "<p>x</p>", {})["content"] == "ok"
