"""Execute the Python 2.0.1 reference for each fixture; emit output + hash.

Usage: PYTHONPATH=<py201> python run_python.py fixtures.json > python_results.json
"""
import json
import sys

import webweavex as w
from core.crypto.kaalka_hash_engine import compute_kaalka_hash as H


def call(api, args):
    fn = getattr(w, api)
    cleaned = [a for a in args]
    if api == "extract_kubernetes_runtime":
        return fn(cleaned[0])
    if api == "extract_database_runtime":
        return fn(cleaned[0], cleaned[1] if len(cleaned) > 1 else None)
    if api == "build_runtime_memory":
        return fn(cleaned[0], cleaned[1], cleaned[2])
    if api == "query_runtime_memory":
        return fn(cleaned[0], cleaned[1], cleaned[2])
    if api == "build_browser_identity":
        return fn(cleaned[0])
    if api == "compute_kaalka_hash":
        return fn(cleaned[0])
    if api == "compute_global_runtime_fingerprint":
        return fn(cleaned[0], cleaned[1], cleaned[2], cleaned[3], cleaned[4],
                  cleaned[5])
    if api == "query_runtime_graph":
        return fn(cleaned[0], cleaned[1])
    if api == "validate_replay_equivalence":
        return fn(cleaned[0], cleaned[1])
    if api == "reconstruct_runtime":
        return fn(cleaned[0], cleaned[1], cleaned[2], cleaned[3], cleaned[4],
                  cleaned[5], cleaned[6], cleaned[7])
    if api == "get_runtime_kernel":
        # Canonical observable kernel state (the rest are methods).
        return {"runtime_type": fn(cleaned[0]).runtime_type}
    if api in ("extract_container_runtime", "extract_ide_runtime"):
        return fn(cleaned[0], cleaned[1] if len(cleaned) > 1 else None)
    raise SystemExit("unknown api " + api)


def main():
    fixtures = json.load(open(sys.argv[1], encoding="utf-8"))
    out = []
    for fx in fixtures:
        try:
            result = call(fx["api"], fx["args"])
            out.append({
                "id": fx["id"], "api": fx["api"],
                "output": result,
                "hash": result if fx["api"] == "compute_kaalka_hash" else H(result),
            })
        except Exception as e:  # noqa: BLE001
            out.append({"id": fx["id"], "api": fx["api"],
                        "error": f"{type(e).__name__}: {e}"})
    print(json.dumps(out, ensure_ascii=False))


if __name__ == "__main__":
    main()
