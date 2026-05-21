from core.auth.authentication_runtime_engine import rotate_authenticated_session
from core.browser import universal_web_extraction_engine as web_engine
from core.ir.browser_ir import compile_browser_ir


class _MockPage:
    context = None


def test_deterministic_session_hash():
    session = {
        "cookies": [{"name": "sid", "value": "1"}],
        "headers": {},
        "auth_tokens": [],
    }

    first = compile_browser_ir(
        runtime={"url": "https://example.com", "title": "Example"},
        dom={"nodes": []},
        extraction={},
        network={"requests": []},
        session=session,
        authenticated=True,
    )
    second = compile_browser_ir(
        runtime={"url": "https://example.com", "title": "Example"},
        dom={"nodes": []},
        extraction={},
        network={"requests": []},
        session=session,
        authenticated=True,
    )

    assert first["session_fingerprint"] == second["session_fingerprint"]


def test_authenticated_extraction_mock(tmp_path, monkeypatch):
    session = {
        "cookies": [{"name": "sid", "value": "abc"}],
        "headers": {},
        "auth_tokens": [],
        "authenticated": True,
    }

    def fake_render(url, session=None, authenticated=False, **_kwargs):
        updated = rotate_authenticated_session(session or {})
        return {
            "available": True,
            "url": url,
            "title": "Dashboard",
            "html": "<html><body>dashboard</body></html>",
            "network": {"requests": [], "bounded": True},
            "session": updated,
            "authenticated": authenticated,
            "bounded": True,
        }

    monkeypatch.setattr(
        web_engine,
        "render_page",
        fake_render,
    )

    path = tmp_path / "session.enc"
    key = "kaalka-test-key"

    from core.session.encrypted_session_store import save_encrypted_session

    save_encrypted_session(str(path), session, key)

    result = web_engine.extract_web(
        "https://example.com/dashboard",
        authenticated=True,
        session_path=str(path),
        encryption_key=key,
    )

    assert result["authenticated"] is True
    assert result["session_persisted"] is True
    assert result["browser_ir"]["authenticated"] is True
    assert result["runtime"]["available"] is True
