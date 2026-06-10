"""Cross-language verifier — Python runner.

Usage: set PYTHONPATH to the materialized python branch, then
    python run_python.py vectors.json out_python.json
"""
import json
import sys

from core.determinism.normalization import stable_serialize
from core.crypto.kaalka_runtime_engine import (
    compute_deterministic_hash,
    derive_kaalka_time_key,
    decrypt_value,
    encrypt_value,
)
from core.crypto.kaalka_engine import hex_fingerprint
from core.serialize.deterministic_serializer import dumps_deterministic


def main():
    spec = json.load(open(sys.argv[1], encoding="utf-8"))
    key = spec["key"]
    out = {"time_key": derive_kaalka_time_key(key), "vectors": {}}
    for vid in sorted(spec["vectors"]):
        v = spec["vectors"][vid]
        enc = encrypt_value(v, key)["encrypted"]
        out["vectors"][vid] = {
            "stable": stable_serialize(v),
            "canonical": dumps_deterministic(v),
            "hash": compute_deterministic_hash(v),
            "encrypted_b64": enc,
            "roundtrip_ok": decrypt_value(enc, key)["decrypted"] == stable_serialize(v),
            "fingerprint_hex": hex_fingerprint(v),
        }
    with open(sys.argv[2], "wb") as f:
        f.write(json.dumps(out, ensure_ascii=False, sort_keys=True, indent=1).encode("utf-8"))


if __name__ == "__main__":
    main()
