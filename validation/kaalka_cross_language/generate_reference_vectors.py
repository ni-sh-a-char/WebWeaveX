#!/usr/bin/env python3
"""Generate Kaalka reference vectors for cross-language validation."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from core.crypto.kaalka_runtime_engine import encrypt_value, decrypt_value
from core.crypto.kaalka_hash_engine import compute_kaalka_hash


def main() -> int:
    fixtures = json.loads((Path(__file__).parent / "fixtures.json").read_text(encoding="utf-8"))
    vectors = []
    for item in fixtures["vectors"]:
        enc = encrypt_value(item["plaintext"], item["key"])
        dec = decrypt_value(enc["encrypted"], item["key"])
        vectors.append(
            {
                "id": item["id"],
                "encrypted": enc["encrypted"],
                "hash": compute_kaalka_hash(item["plaintext"]),
                "decrypt_ok": dec["decrypted"] == item["plaintext"],
            }
        )
    out = {
        "language": "python",
        "algorithm": "kaalka",
        "vectors": vectors,
    }
    path = Path(__file__).parent / "reference_vectors.json"
    path.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"Wrote {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
