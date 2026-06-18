#!/usr/bin/env python3
"""Session-8 cross-language golden vectors from canonical Python 2.1.0.

Run from a materialized Python-branch checkout (so `core` is importable):

    python tools/gen_java_parity_vectors_s8.py <out.json>

Covers the session-crypto cluster (which forces the JDK-only json.loads substrate):
encrypt_session_state / decrypt_session_state (core.crypto.kaalka_session_engine) and
save_encrypted_session / load_encrypted_session (core.session.encrypted_session_store).

encrypt/decrypt are byte-exact VECTOR proofs (stable_serialize + compute_kaalka_hash).
save records the exact written file content (json.dumps(payload, sort_keys=True)); load
records the recovered-output serialize+hash. All values originate from canonical Python.
"""
from __future__ import annotations

import json
import os
import sys
import tempfile

from core.crypto.kaalka_hash_engine import compute_kaalka_hash
from core.determinism.normalization import stable_serialize

from core.crypto.kaalka_session_engine import encrypt_session_state, decrypt_session_state
from core.session.encrypted_session_store import save_encrypted_session, load_encrypted_session

KEY = "session-key-2024"

# Session shapes — chosen to exercise json.loads value branches via real round-trips:
# empty, flags, nested dict, list-of-dicts, unicode, numbers (int/float/neg), big-int,
# non-finite (Infinity), bool/null, ordering.
SESSIONS = [
    ("sess_empty", {}),
    ("sess_flags", {"authenticated": True, "version": 1}),
    ("sess_cookies", {"cookies": [{"name": "sid", "value": "abc"}, {"name": "csrf", "value": "z"}],
                      "authenticated": False}),
    ("sess_nested_headers", {"headers": {"User-Agent": "wx", "Accept": "*/*"},
                             "auth_tokens": ["t1", "t2"], "local_storage": {"k": "v"}}),
    ("sess_unicode", {"user": "用户", "note": "café \U0001F600", "ключ": "значение"}),
    ("sess_numbers", {"count": 42, "ratio": 0.5, "scientific": 1e3, "neg": -7, "zero": 0}),
    ("sess_bigint", {"id": 10 ** 25, "small": 1}),
    ("sess_nonfinite", {"inf": float("inf"), "ninf": float("-inf")}),
    ("sess_bool_null", {"x": None, "y": True, "z": False, "list": [None, True, False]}),
    ("sess_ordering", {"z": 1, "a": 2, "m": 3, "B": 4}),
    ("sess_deep_nested", {"a": {"b": {"c": [1, 2, {"d": "deep"}]}}}),
    ("sess_escapes", {"path": "a\tb\nc\"d\\e", "ctrl": "xy"}),
]


def main() -> None:
    out = {"source": "Python 2.1.0 canonical (session 8: session crypto + json.loads substrate)"}

    encrypt_vecs, decrypt_vecs = [], []
    for name, session in SESSIONS:
        payload = encrypt_session_state(session, KEY)
        encrypt_vecs.append({
            "name": name, "inputs": {"session": session, "key": KEY},
            "serialized": stable_serialize(payload), "hash": compute_kaalka_hash(payload)})
        dec = decrypt_session_state(payload, KEY)
        decrypt_vecs.append({
            "name": name, "inputs": {"payload": payload, "key": KEY},
            "serialized": stable_serialize(dec), "hash": compute_kaalka_hash(dec)})
    out["encrypt_session_state"] = encrypt_vecs
    out["decrypt_session_state"] = decrypt_vecs

    # save/load — exercise the real filesystem path in a temp dir.
    save_vecs, load_vecs = [], []
    d = tempfile.mkdtemp(prefix="wwx_s8_")
    for name, session in SESSIONS[:6]:
        fname = name + ".json"
        p = os.path.join(d, fname)
        save_encrypted_session(p, session, KEY)
        with open(p, encoding="utf-8") as fh:
            file_content = fh.read()
        save_vecs.append({
            "name": name, "inputs": {"filename": fname, "session": session, "key": KEY},
            "file_content": file_content})
        load_ret = load_encrypted_session(p, KEY)
        load_vecs.append({
            "name": "load_" + name, "file_content": file_content, "key": KEY,
            "serialized": stable_serialize(load_ret), "hash": compute_kaalka_hash(load_ret)})
    # missing file
    miss = load_encrypted_session(os.path.join(d, "does_not_exist.json"), KEY)
    load_vecs.append({
        "name": "load_missing", "missing": True, "key": KEY,
        "serialized": stable_serialize(miss), "hash": compute_kaalka_hash(miss)})

    out["save_encrypted_session"] = save_vecs
    out["load_encrypted_session"] = load_vecs

    # json.loads substrate parity — Python json.loads is the oracle. Covers every value
    # branch (incl. surrogate pairs, big int, floats, non-finite, whitespace, nesting) and
    # malformed inputs that must raise (parity: Python json.loads also raises).
    valid_texts = [
        "null", "true", "false", "0", "123", "-5", "3.14", "-2.5", "1e10", "1E-3", "1.0",
        "\"hi\"", "\"\\u00e9\"", "\"\\ud83d\\ude00\"", "\"a\\tb\\nc\"", "\"\"",
        "[]", "{}", "[1, 2, 3]", "[1,2.5,true,null,\"x\"]",
        "{\"a\":1,\"b\":[true,null],\"c\":{\"d\":\"e\"}}",
        "  42  ", "123456789012345678901234567890", "NaN", "Infinity", "-Infinity",
        "{\"\\u00fc\":\"\\u00f1\"}", "[[[[1]]]]",
    ]
    invalid_texts = [
        "", "{", "[1,2", "{\"a\"}", "{\"a\":}", "tru", "123abc", "[,]", "\"unterminated",
        "{\"a\":1,}", "nul", "[1 2]",
    ]
    jl = []
    for i, text in enumerate(valid_texts):
        val = json.loads(text)
        jl.append({"name": f"valid_{i}", "text": text, "error": False,
                   "serialized": stable_serialize(val), "hash": compute_kaalka_hash(val)})
    for i, text in enumerate(invalid_texts):
        raised = False
        try:
            json.loads(text)
        except Exception:
            raised = True
        jl.append({"name": f"invalid_{i}", "text": text, "error": True, "raises_in_python": raised})
    out["json_loads"] = jl

    target = sys.argv[1] if len(sys.argv) > 1 else "golden_vectors_s8.json"
    with open(target, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    counts = {k: len(v) for k, v in out.items() if isinstance(v, list)}
    sys.stderr.write(f"wrote {target}: {sum(counts.values())} vectors {counts}\n")


if __name__ == "__main__":
    main()
