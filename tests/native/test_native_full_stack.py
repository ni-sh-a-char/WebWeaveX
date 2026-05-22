"""Native runtime orchestrator branch coverage."""

from core.native.native_runtime_orchestrator import extract_native, run_native_cognition


def test_run_native_cognition_platforms():
    for runtime in ("desktop", "terminal", "electron", "vm", "remote"):
        out = run_native_cognition(runtime=runtime, application="app", snapshot={"bounded": True})
        assert out.get("bounded") is True


def test_extract_native_all_runtimes(tmp_path):
    key = "native-key"
    path = str(tmp_path / "native.kaalka")
    for runtime, snap in [
        ("desktop", None),
        ("terminal", {"output": ["$"], "commands": [], "prompts": ["$"]}),
        ("electron", {"routes": [{"path": "/"}], "ipc": []}),
        ("vm", {"guest": "linux"}),
        ("remote", {"protocol": "ssh", "host": "x"}),
    ]:
        out = extract_native(
            runtime=runtime,
            application="app",
            snapshot=snap,
            persistent_runtime=True,
            runtime_path=path,
            runtime_key=key,
            application_cognition=True,
            causality_runtime=True,
            semantic_runtime=True,
            autonomous_workflow=True,
            synchronized_runtime=True,
            evolving_runtime=True,
            federated_memory=True,
            execution_runtime=True,
            simulate_execution=True,
            reconstruction_runtime=True,
            fabricate_runtime=True,
            clone_runtime=True,
            causal_memory_path=str(tmp_path / "c.kaalka"),
            semantic_memory_path=str(tmp_path / "s.kaalka"),
            workflow_memory_path=str(tmp_path / "w.kaalka"),
            sync_memory_path=str(tmp_path / "sy.kaalka"),
            evolution_memory_path=str(tmp_path / "e.kaalka"),
            federated_memory_path=str(tmp_path / "f.kaalka"),
            execution_memory_path=str(tmp_path / "ex.kaalka"),
            reconstruction_memory_path=str(tmp_path / "r.kaalka"),
            causal_memory_key=key,
            semantic_memory_key=key,
            workflow_memory_key=key,
            sync_memory_key=key,
            evolution_memory_key=key,
            federated_memory_key=key,
            execution_memory_key=key,
            reconstruction_memory_key=key,
        )
        assert out.get("bounded") is True
