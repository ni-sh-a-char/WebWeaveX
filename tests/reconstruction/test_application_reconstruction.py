from core.reconstruction.application_reconstruction_engine import reconstruct_application_runtime


def test_application_reconstruction():
    result = reconstruct_application_runtime(
        application_ir={"forms": {"login": {}}, "dashboards": ["main"]},
        workflow_ir={"objective": "operate"},
        runtime_type="browser",
    )

    assert result["replay_safe"] is True
    assert result["runtime_type"] == "browser"
