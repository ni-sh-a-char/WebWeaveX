from core.reconstruction.runtime_identity_reconstruction import reconstruct_runtime_identity


def test_identity_continuity():
    browser = {"identity_id": "browser-1", "fingerprint": "fp-a"}
    session = {"session_id": "sess-1", "authenticated": True}

    first = reconstruct_runtime_identity(
        browser_identity=browser,
        session=session,
        runtime_id="rt-1",
        execution_id="ex-1",
        worker_id="w-1",
    )
    second = reconstruct_runtime_identity(
        browser_identity=browser,
        session=session,
        runtime_id="rt-1",
        execution_id="ex-1",
        worker_id="w-1",
    )

    assert first == second
    assert first["browser_identity"]["identity_hash"] == second["browser_identity"]["identity_hash"]
    assert len(first["continuity_hashes"]) == 3
