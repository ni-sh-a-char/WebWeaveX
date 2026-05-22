"""Exercise extract_web optional runtime branches with deterministic mocks."""

from pathlib import Path

import pytest

from core.browser.universal_web_extraction_engine import extract_web


def _mock_runtime(*_a, **_k):
    return {
        "available": True,
        "html": (
            "<html><head><title>T</title></head><body>"
            "<main><a href='/docs'>Docs</a><button id='go'>Go</button></main>"
            "</body></html>"
        ),
        "network": {"requests": [{"url": "https://example.com/", "method": "GET"}]},
        "cookies": [],
        "route": "/",
    }


@pytest.fixture
def mock_render(monkeypatch):
    monkeypatch.setattr(
        "core.browser.universal_web_extraction_engine.render_page",
        _mock_runtime,
    )


def test_extract_web_all_runtime_flags(tmp_path, mock_render):
    base = tmp_path / "state"
    base.mkdir()
    paths = {
        "session_path": str(base / "sess.kaalka"),
        "interaction_path": str(base / "ix.kaalka"),
        "stream_path": str(base / "stream.kaalka"),
        "identity_path": str(base / "id.kaalka"),
        "adaptation_path": str(base / "adapt.kaalka"),
        "checkpoint_path": str(base / "dist.kaalka"),
        "application_memory_path": str(base / "app.kaalka"),
        "causal_memory_path": str(base / "cau.kaalka"),
        "semantic_memory_path": str(base / "sem.kaalka"),
        "workflow_memory_path": str(base / "wf.kaalka"),
        "sync_memory_path": str(base / "sync.kaalka"),
        "evolution_memory_path": str(base / "evo.kaalka"),
        "live_memory_path": str(base / "live.kaalka"),
        "federated_memory_path": str(base / "fed.kaalka"),
        "execution_memory_path": str(base / "ex.kaalka"),
        "reconstruction_memory_path": str(base / "rec.kaalka"),
    }
    key = "unit-test-key"
    out = extract_web(
        "https://example.com/app",
        authenticated=True,
        encryption_key=key,
        interactions=[{"action": "click", "selector": "#go"}],
        infinite_scroll=True,
        pagination_selector=".next",
        stream_runtime=True,
        websocket_capture=True,
        mutation_capture=True,
        browser_identity=True,
        persistent_identity=True,
        adaptive_runtime=True,
        persistent_adaptation=True,
        selector_healing=True,
        modal_recovery=True,
        pagination_recovery=True,
        distributed_runtime=True,
        autonomous_runtime=True,
        application_cognition=True,
        persistent_application_memory=True,
        causality_runtime=True,
        semantic_runtime=True,
        autonomous_workflow=True,
        synchronized_runtime=True,
        evolving_runtime=True,
        live_runtime=False,
        federated_memory=True,
        execution_runtime=True,
        simulate_execution=True,
        reconstruction_runtime=True,
        fabricate_runtime=True,
        clone_runtime=True,
        interaction_key=key,
        stream_key=key,
        identity_key=key,
        adaptation_key=key,
        checkpoint_key=key,
        application_memory_key=key,
        causal_memory_key=key,
        semantic_memory_key=key,
        workflow_memory_key=key,
        sync_memory_key=key,
        evolution_memory_key=key,
        live_memory_key=key,
        federated_memory_key=key,
        execution_memory_key=key,
        reconstruction_memory_key=key,
        **paths,
    )
    assert out.get("bounded") is True
    assert out.get("global_runtime_fingerprint")
    assert "browser_ir" in out or not out.get("runtime", {}).get("available")


def test_extract_web_preloaded_persistence(tmp_path, mock_render):
    from core.application.application_memory_engine import save_application_memory
    from core.adaptive.extraction_memory_engine import save_adaptive_memory
    from core.distributed_extraction.distributed_checkpoint_engine import (
        save_distributed_checkpoint,
    )
    from core.identity.fingerprint_persistence_engine import save_browser_identity
    from core.interaction.interaction_replay_store import save_interaction_replay
    from core.streaming.stream_persistence_engine import save_stream_runtime

    key = "preload-key"
    base = tmp_path / "pre"
    base.mkdir()
    save_application_memory(str(base / "app.kaalka"), {"workflows": {}}, key)
    save_adaptive_memory(str(base / "adapt.kaalka"), {"selectors": {"a": "#a"}}, key)
    save_distributed_checkpoint(str(base / "dist.kaalka"), {"workers": [{"worker_id": "w0"}]}, key)
    save_browser_identity(str(base / "id.kaalka"), {"user_agent": "ua"}, key)
    save_interaction_replay(str(base / "ix.kaalka"), [{"action": "click"}], key)
    save_stream_runtime(str(base / "stream.kaalka"), {"events": [], "runtime": {}}, key)

    out = extract_web(
        "https://example.com",
        application_cognition=True,
        application_memory_path=str(base / "app.kaalka"),
        application_memory_key=key,
        adaptive_runtime=True,
        adaptation_path=str(base / "adapt.kaalka"),
        adaptation_key=key,
        distributed_runtime=True,
        checkpoint_path=str(base / "dist.kaalka"),
        checkpoint_key=key,
        browser_identity=True,
        identity_path=str(base / "id.kaalka"),
        identity_key=key,
        interaction_path=str(base / "ix.kaalka"),
        interaction_key=key,
        stream_path=str(base / "stream.kaalka"),
        stream_key=key,
    )
    assert out.get("bounded") is True


def test_extract_web_unavailable_runtime(monkeypatch):
    monkeypatch.setattr(
        "core.browser.universal_web_extraction_engine.render_page",
        lambda *a, **k: {"available": False, "reason": "mock"},
    )
    out = extract_web("https://example.com")
    assert out.get("bounded") is True
    assert out.get("available") is False
