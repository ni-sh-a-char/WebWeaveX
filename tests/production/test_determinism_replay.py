from core.contracts.runtime_contracts import UniversalInput
from core.crypto.kaalka_runtime_engine import encrypt_value
from core.determinism.global_runtime_fingerprint import compute_global_runtime_fingerprint
from core.kernel.runtime_pipeline import run_canonical_pipeline
from core.replay.replay_equivalence_engine import validate_replay_equivalence


def test_global_runtime_fingerprint_stable():
    payload = {"unified_runtime_graph": {"nodes": [{"id": "a"}], "edges": []}}
    assert compute_global_runtime_fingerprint(payload) == compute_global_runtime_fingerprint(payload)


def test_kaalka_triple_stable():
    enc = [encrypt_value("x", "k")["encrypted"] for _ in range(5)]
    assert len(set(enc)) == 1


def test_replay_equivalence_self():
    sample = {
        "unified_runtime_graph": {"nodes": [{"id": "n1"}], "edges": []},
        "browser_ir": {"runtime_identity": "abc123"},
    }
    result = validate_replay_equivalence(sample, sample)
    assert result["equivalent"] is True


def test_canonical_pipeline_fingerprint():
    out = run_canonical_pipeline(
        UniversalInput(source="https://example.com", source_type="web"),
        options={"kernel": {"semantic": False, "sync": False, "memory": False, "execution": False, "reconstruction": False}},
    )
    fp = compute_global_runtime_fingerprint(out)
    assert fp
    assert out["pipeline_hash"]
