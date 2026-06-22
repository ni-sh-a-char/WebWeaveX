#!/usr/bin/env python3
"""Session-17 cross-language golden vectors from canonical Python 2.1.0.

    python tools/gen_java_parity_vectors_s17.py <out.json>

Covers the 4 dependency-clean memory-persistence engine pairs (save/load for runtime, semantic,
adaptive, application memory). Python is the oracle; save records file content byte-exact, load
records the recovered output + the missing-file branch.
"""
from __future__ import annotations

import json
import os
import sys
import tempfile

from core.crypto.kaalka_hash_engine import compute_kaalka_hash
from core.determinism.normalization import stable_serialize

from core.memory.runtime_memory_persistence_engine import save_runtime_memory, load_runtime_memory
from core.semantic.semantic_memory_engine import save_semantic_memory, load_semantic_memory
from core.adaptive.extraction_memory_engine import save_adaptive_memory, load_adaptive_memory
from core.application.application_memory_engine import save_application_memory, load_application_memory

KEY = "mem-key-2024"

ENGINES = [
    ("runtime", save_runtime_memory, load_runtime_memory),
    ("semantic", save_semantic_memory, load_semantic_memory),
    ("adaptive", save_adaptive_memory, load_adaptive_memory),
    ("application", save_application_memory, load_application_memory),
]

MEMS = [
    ("simple", {"runtime": {"a": 1}, "bounded": True}),
    ("unicode", {"note": "café \U0001F600", "用户": 1, "nested": {"k": [1, 2, 3]}, "bounded": True}),
    ("empty", {}),
]


def main() -> None:
    out = {"source": "Python 2.1.0 canonical (session 17: memory persistence x4)"}

    d = tempfile.mkdtemp(prefix="wwx_s17_")
    for engine, save_fn, load_fn in ENGINES:
        save_vecs, load_vecs = [], []
        for nm, mem in MEMS:
            fname = f"{engine}_{nm}.json"
            p = os.path.join(d, fname)
            save_fn(p, mem, KEY)
            with open(p, encoding="utf-8") as fh:
                content = fh.read()
            save_vecs.append({"name": nm, "inputs": {"filename": fname, "memory": mem, "key": KEY},
                              "file_content": content})
            load_ret = load_fn(p, KEY)
            load_vecs.append({"name": "load_" + nm, "file_content": content, "key": KEY,
                              "serialized": stable_serialize(load_ret), "hash": compute_kaalka_hash(load_ret)})
        miss = load_fn(os.path.join(d, f"{engine}_nope.json"), KEY)
        load_vecs.append({"name": "load_missing", "missing": True, "key": KEY,
                          "serialized": stable_serialize(miss), "hash": compute_kaalka_hash(miss)})
        out[f"save_{engine}_memory"] = save_vecs
        out[f"load_{engine}_memory"] = load_vecs

    target = sys.argv[1] if len(sys.argv) > 1 else "golden_vectors_s17.json"
    with open(target, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    counts = {k: len(v) for k, v in out.items() if isinstance(v, list)}
    sys.stderr.write(f"wrote {target}: {sum(counts.values())} vectors across {len(counts)} sections\n")


if __name__ == "__main__":
    main()
