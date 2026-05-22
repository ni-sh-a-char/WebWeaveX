"""Auth, pipeline, unified IR, and intelligence coverage."""

import pytest

from core.auth.authentication_runtime_engine import authenticate_runtime, rotate_authenticated_session
from core.ir.unified_runtime_ir import compile_unified_runtime_ir
from core.kernel.runtime_pipeline import run_canonical_pipeline
from core.contracts.runtime_contracts import UniversalInput
from webweavex.plugins.intelligence_engine import run_ai_task, build_prompt


def test_authenticate_form_login():
    class _El:
        def fill(self, *_a, **_k):
            return None

        def click(self, *_a, **_k):
            return None

    class _Page:
        def locator(self, sel):
            return _El()

    out = authenticate_runtime(
        _Page(),
        {"username": "u", "password": "p"},
        {
            "method": "form_login",
            "username_selector": "#u",
            "password_selector": "#p",
            "submit_selector": "#s",
        },
    )
    assert out.get("bounded") is True


def test_rotate_session():
    out = rotate_authenticated_session({"cookies": [], "rotation_index": 0})
    assert out.get("rotation_index") == 1


def test_unified_runtime_ir():
    ir = compile_unified_runtime_ir(
        registry={"phases": {"semantic": {"entities": []}, "memory": {}}},
        graph={"nodes": [{"id": "n1"}], "edges": []},
        bus=[{"tick": 1, "order": 0, "phase": "semantic"}],
        phase_results=[{"phase": "semantic", "bounded": True}],
        sources={"browser": {"url": "https://example.com"}, "workflow": {"steps": []}},
    )
    assert ir.get("ir") == "unified_runtime"
    assert ir.get("runtime_graph", {}).get("nodes")


def test_canonical_pipeline_text():
    out = run_canonical_pipeline(UniversalInput(source="hello world", source_type="text"))
    assert out.get("pipeline_hash")


def test_intelligence_provider_paths(monkeypatch):
    data = {"human_readable": "text", "structured_data": {"text": "sample"}}
    assert build_prompt("extract_entities", data)

    class _Prov:
        @staticmethod
        def generate(prompt, config):
            return "ok"

    monkeypatch.setattr(
        "webweavex.plugins.intelligence_engine._load_provider",
        lambda _n: _Prov,
    )
    out = run_ai_task(data, "analyze", "groq", {})
    assert out.get("success") is True
