#!/usr/bin/env python3
"""Generate cross-language parity golden vectors from canonical Python 2.1.0.

Run from a materialized Python-branch checkout (so `core` is importable):

    python tools/gen_java_parity_vectors.py > golden_vectors.json

Each "vectors" entry stores the raw input (JSON-roundtrippable), the canonical
`stable_serialize` output, and the `compute_kaalka_hash` digest. The Java test
parses `input`, recomputes both, and asserts byte-equality. Crypto vectors carry
the derived time key and base64 ciphertext for the Kaalka v5 byte path.
"""
from __future__ import annotations

import json
import math
import sys

from core.crypto.kaalka_hash_engine import compute_kaalka_hash
from core.crypto.kaalka_runtime_engine import (
    KAALKA_ALGORITHM,
    derive_kaalka_time_key,
    encrypt_value,
)
from core.determinism.normalization import stable_serialize

# (name, value) — every value here is JSON-roundtrippable so Jackson can
# reconstruct the identical native type tree on the Java side.
VECTORS = [
    ("string_plain", "hello"),
    ("string_unicode", "café \U0001F680 中文"),
    ("string_crlf", "a\r\nb\rc\n"),
    ("string_trailing_ws", "trim me   \t  "),
    ("string_nfkc", "ﬁ ① ²"),  # ﬁ ① ²  -> NFKC folds
    ("int_zero", 0),
    ("int_pos", 42),
    ("int_neg", -987654321),
    ("int_big", 9007199254740993),
    ("float_simple", 0.1),
    ("float_neg", -2.5),
    ("float_repr", 1234567.89),
    ("float_sci_large", 1e20),
    ("float_sci_small", 1e-7),
    ("float_integral", 2.0),
    ("float_integral_big", 9007199254740991.0),
    ("bool_true", True),
    ("bool_false", False),
    ("null", None),
    ("empty_obj", {}),
    ("empty_arr", []),
    ("obj_sorted", {"b": 1, "a": 2.0, "c": "x"}),
    ("obj_volatile", {"timestamp": 99, "data": 1, "nonce": "z", "keep": True}),
    ("obj_nested", {"z": {"y": 2, "x": 1}, "a": [3, 2, 1]}),
    ("arr_scalars", [3, "x", True, None, 2.0]),
    ("arr_of_objs", [{"z": 1, "a": 2}, {"timestamp": 5, "b": 9}]),
    ("arr_nested", [[1, 2], [3, {"k": 1}]]),
    ("deep_unicode_keys", {"\U0001F600": 1, "a": 2, "é": 3}),
    ("mixed_numbers", {"i": 7, "f": 3.14, "big_int_float": 1e16, "neg": -0.5}),
]

CRYPTO = [
    ("crypt_obj", {"k": "v"}, "secret"),
    ("crypt_string", "payload", "another-key"),
    ("crypt_unicode", {"msg": "café \U0001F680"}, "kéy"),
    ("crypt_nested", {"a": [1, 2, {"b": 3}]}, "p@ss"),
]


def main() -> None:
    vectors = []
    for name, value in VECTORS:
        vectors.append(
            {
                "name": name,
                "input": value,
                "serialized": stable_serialize(value),
                "hash": compute_kaalka_hash(value),
            }
        )

    # Non-JSON scalars (NaN / Infinity) — Java test constructs these directly.
    specials = []
    for name, value in [("nan", math.nan), ("inf", math.inf), ("neg_inf", -math.inf)]:
        specials.append(
            {
                "name": name,
                "serialized": stable_serialize(value),
                "hash": compute_kaalka_hash(value),
            }
        )

    crypto = []
    for name, value, key in CRYPTO:
        env = encrypt_value(value, key)
        crypto.append(
            {
                "name": name,
                "input": value,
                "key": key,
                "time_key": derive_kaalka_time_key(key),
                "encrypted": env["encrypted"],
                "hash": compute_kaalka_hash(value),
            }
        )

    out = {
        "source": "Python 2.1.0 canonical (compute_kaalka_hash == compute_deterministic_hash)",
        "algorithm": KAALKA_ALGORITHM,
        "vectors": vectors,
        "special_scalars": specials,
        "crypto": crypto,
    }
    target = sys.argv[1] if len(sys.argv) > 1 else "golden_vectors.json"
    with open(target, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    sys.stderr.write(
        f"wrote {len(vectors)} vectors, {len(specials)} specials, "
        f"{len(crypto)} crypto -> {target}\n"
    )


if __name__ == "__main__":
    main()
