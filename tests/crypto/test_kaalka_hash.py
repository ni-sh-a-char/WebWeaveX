from core.crypto.kaalka_hash_engine import (
    compute_kaalka_hash,
    compute_kaalka_hash_payload,
)


def test_compute_kaalka_hash_deterministic():
    first = compute_kaalka_hash("WebWeaveX")
    second = compute_kaalka_hash("WebWeaveX")

    assert first == second
    assert len(first) == 64


def test_compute_kaalka_hash_payload_sorted():
    payload_a = {"b": 2, "a": 1}
    payload_b = {"a": 1, "b": 2}

    assert (
        compute_kaalka_hash_payload(payload_a)
        == compute_kaalka_hash_payload(payload_b)
    )
