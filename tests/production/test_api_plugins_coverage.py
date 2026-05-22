"""Coverage for webweavex.api and webweavex.plugins surfaces."""

import pytest

from webweavex.api.schemas import validate_request, validate_response
from webweavex.api.config import STRICT_CRE_DEFAULT, DEFAULT_FALLBACK
from webweavex.plugins.intelligence_engine import (
    build_prompt,
    run_ai_task,
    enhanced_task_runner,
    _mock_ai_response,
    _fallback_to_rule,
)
from webweavex.plugins import (
    Plugin,
    register_plugin,
    execute_plugins,
    list_plugins,
    load_provider,
)


def test_validate_request_and_response():
    req = validate_request({"input": "hello", "mode": "compiler"})
    assert req["input"] == "hello"
    resp = validate_response(
        {
            "structured_data": {},
            "confidence": 0.9,
            "source": "test",
            "version": "2.0.0",
        }
    )
    assert resp["confidence"] == 0.9


def test_api_config_defaults():
    assert isinstance(STRICT_CRE_DEFAULT, bool)
    assert "structured_data" in DEFAULT_FALLBACK


def test_intelligence_engine_mock_and_rules():
    data = {"structured_data": {"text": "sample"}, "human_readable": "sample"}
    assert "sample" in build_prompt("summarize", data)
    mock = run_ai_task(data, "summarize", "mock", {})
    assert mock["success"] is True
    rule = _fallback_to_rule("analyze", data)
    assert rule["fallback"] is True
    assert _mock_ai_response("summarize", data)["provider"] == "mock"
    out = enhanced_task_runner(data, "summarize", provider=None)
    assert "summary" in out or "result" in str(out)


def test_intelligence_unknown_provider():
    with pytest.raises(ValueError):
        run_ai_task({"human_readable": "x"}, "analyze", "not_a_provider", {})


def test_plugins_execute_and_load_provider_error():
    class _P(Plugin):
        name = "cov_plugin"

        def execute(self, data, config):
            data["ok"] = True
            return data

    register_plugin("cov_plugin", _P())
    out = execute_plugins({"x": 1}, ["cov_plugin"])
    assert out["ok"] is True
    assert "cov_plugin" in list_plugins()
    with pytest.raises(ValueError):
        load_provider("unknown_provider_xyz")


def test_api_run_non_strict(monkeypatch):
    from webweavex.api import api as api_mod

    def _boom(*_a, **_k):
        raise RuntimeError("pipeline down")

    monkeypatch.setattr(api_mod, "run_pipeline", _boom)
    out = api_mod.run({"input": "test", "mode": "compiler"})
    assert out["confidence"] == 0.0
