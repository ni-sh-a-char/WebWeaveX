#!/usr/bin/env python3
"""Session-18 cross-language golden vectors from canonical Python 2.1.0.

    python tools/gen_java_parity_vectors_s18.py <out.json>

Covers the dependency-clean core.identity family: build_browser_identity (orchestrator over ~11
fingerprint engines) + save/load_browser_identity persistence. Python is the oracle.
"""
from __future__ import annotations

import json
import os
import sys
import tempfile

from core.crypto.kaalka_hash_engine import compute_kaalka_hash
from core.determinism.normalization import stable_serialize

from core.identity.browser_identity_orchestrator import build_browser_identity
from core.identity.fingerprint_persistence_engine import save_browser_identity, load_browser_identity
from core.identity.browser_profile_engine import build_browser_profile
from core.identity.user_agent_runtime_engine import build_user_agent_runtime
from core.identity.platform_runtime_engine import build_platform_runtime
from core.identity.language_runtime_engine import build_language_runtime
from core.identity.timezone_runtime_engine import build_timezone_runtime
from core.identity.webgl_runtime_engine import build_webgl_runtime
from core.identity.canvas_runtime_engine import build_canvas_runtime
from core.identity.font_runtime_engine import build_font_runtime
from core.identity.media_device_runtime_engine import build_media_device_runtime
from core.identity.navigator_runtime_engine import build_navigator_runtime
from core.identity.browser_entropy_engine import compute_runtime_entropy, normalize_browser_fingerprint
from core.identity.browser_fingerprint_engine import fingerprint_browser_identity

KEY = "id-key-2024"
PROFILES = ["default", "profile_a", "profile_b", "unknown_profile"]


def ev(name, inputs, value):
    return {"name": name, "inputs": inputs,
            "serialized": stable_serialize(value), "hash": compute_kaalka_hash(value)}


def main() -> None:
    out = {"source": "Python 2.1.0 canonical (session 18: browser identity)"}

    out["build_browser_identity"] = [
        ev("identity_" + p, {"profile_id": p}, build_browser_identity(p)) for p in PROFILES
    ]

    # ---- engine-level parity ----
    def per_profile(section, fn):
        out[section] = [ev(section + ":" + p, {"profile_id": p}, fn(p)) for p in PROFILES]

    per_profile("build_browser_profile", build_browser_profile)
    per_profile("build_user_agent_runtime", build_user_agent_runtime)
    per_profile("build_platform_runtime", build_platform_runtime)
    per_profile("build_language_runtime", build_language_runtime)
    per_profile("build_timezone_runtime", build_timezone_runtime)
    per_profile("build_webgl_runtime", build_webgl_runtime)
    per_profile("build_canvas_runtime", build_canvas_runtime)
    per_profile("build_font_runtime", build_font_runtime)
    per_profile("build_media_device_runtime", build_media_device_runtime)
    per_profile("build_navigator_runtime", build_navigator_runtime)

    IDENTITY = build_browser_identity("default")
    # entropy: observed=None and observed=different
    out["compute_runtime_entropy"] = [
        ev("entropy_baseline", {"identity": IDENTITY, "observed": None},
           compute_runtime_entropy(IDENTITY, None)),
        ev("entropy_stable", {"identity": IDENTITY, "observed": IDENTITY},
           compute_runtime_entropy(IDENTITY, IDENTITY)),
        ev("entropy_drift", {"identity": IDENTITY, "observed": build_browser_identity("profile_a")},
           compute_runtime_entropy(IDENTITY, build_browser_identity("profile_a"))),
    ]
    out["normalize_browser_fingerprint"] = [
        ev("normalize", {"identity": IDENTITY}, normalize_browser_fingerprint(IDENTITY)),
        ev("normalize_mixed", {"identity": {"A": "UPPER", "list": ["Z", "a"], "num": 8,
                                            "flag": False, "dict": {"K2": 1, "K1": 2}, "bounded": True}},
           normalize_browser_fingerprint({"A": "UPPER", "list": ["Z", "a"], "num": 8,
                                          "flag": False, "dict": {"K2": 1, "K1": 2}, "bounded": True})),
    ]
    out["fingerprint_browser_identity"] = [
        ev("fingerprint", {"identity": IDENTITY}, {"fingerprint_hash": fingerprint_browser_identity(IDENTITY)}),
    ]

    # save/load_browser_identity (real FS)
    save_vecs, load_vecs = [], []
    d = tempfile.mkdtemp(prefix="wwx_s18_")
    cases = [("simple", build_browser_identity("default")),
             ("profile_b", build_browser_identity("profile_b")),
             ("unicode", {"profile_id": "x", "note": "café \U0001F600", "用户": 1, "bounded": True})]
    for nm, ident in cases:
        fname = nm + ".json"
        p = os.path.join(d, fname)
        save_browser_identity(p, ident, KEY)
        with open(p, encoding="utf-8") as fh:
            content = fh.read()
        save_vecs.append({"name": nm, "inputs": {"filename": fname, "identity": ident, "key": KEY},
                          "file_content": content})
        load_ret = load_browser_identity(p, KEY)
        load_vecs.append({"name": "load_" + nm, "file_content": content, "key": KEY,
                          "serialized": stable_serialize(load_ret), "hash": compute_kaalka_hash(load_ret)})
    miss = load_browser_identity(os.path.join(d, "nope.json"), KEY)
    load_vecs.append({"name": "load_missing", "missing": True, "key": KEY,
                      "serialized": stable_serialize(miss), "hash": compute_kaalka_hash(miss)})
    out["save_browser_identity"] = save_vecs
    out["load_browser_identity"] = load_vecs

    target = sys.argv[1] if len(sys.argv) > 1 else "golden_vectors_s18.json"
    with open(target, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    counts = {k: len(v) for k, v in out.items() if isinstance(v, list)}
    sys.stderr.write(f"wrote {target}: {sum(counts.values())} vectors across {len(counts)} sections\n")


if __name__ == "__main__":
    main()
