"""Cross-product driver — Python side.

For every validation/parity/*_api_vectors.json vector: execute the API live
on the python branch, recompute det_hash, compare with the committed value
(which the Dart test suite asserts), and export the python call signature so
the JS driver can call positionally. Emits cross_python_results.json +
api_signatures.json.
"""
import inspect
import json
import sys
from pathlib import Path

sys.path.insert(0, r"C:\Projects\wwx_cert_py")
import webweavex as w
from core.crypto.kaalka_hash_engine import compute_kaalka_hash as H
from core.execution.runtime_permissions_engine import build_runtime_permissions

VEC_DIR = Path(r"C:\Projects\WebWeaveX\validation\parity")
SKIP = {"python_vectors.json", "javascript_vectors.json", "dart_vectors.json", "parity_report.md"}


# Per-API call shapes mirroring test/parity/*_parity_test.dart adapters exactly.
ADAPTERS = {
    "replay_interactions": lambda v: w.replay_interactions(None, v["input"]["interaction_log"]),
    "replay_stream_events": lambda v: w.replay_stream_events(None, v["input"]["stream_log"]),
    "decrypt_session_state": lambda v: w.decrypt_session_state(
        w.encrypt_session_state(v["input"]["session"], v["input"]["key"]), v["input"]["key"]),
    "execute_runtime_action": lambda v: w.execute_runtime_action(
        v["input"]["raw_action"],
        sandbox=w.build_runtime_sandbox(runtime=v["input"]["sandbox"]) if "sandbox" in v["input"] else None,
        permissions=build_runtime_permissions(scopes=v["input"]["permissions"]) if "permissions" in v["input"] else None,
        tick=v["input"].get("tick", 0)),
    "simulate_runtime_execution": lambda v: w.simulate_runtime_execution(
        v["input"]["actions"],
        sandbox=w.build_runtime_sandbox(runtime=v["input"]["sandbox"]) if "sandbox" in v["input"] else None,
        tick=v["input"].get("tick", 0)),
    "get_runtime_kernel": lambda v: {"runtime_type": w.get_runtime_kernel(*v.get("args", [])).runtime_type},
    "analyze": lambda v: w.analyze(v["input"]["nodes"], v["input"].get("edges")),
}


def call(fn, v):
    if v["api"] in ADAPTERS:
        return ADAPTERS[v["api"]](v), "adapter"
    if "args" in v:
        return fn(*v["args"]), "args"
    inp = v["input"]
    if isinstance(inp, dict):
        try:
            return fn(**inp), "kwargs"
        except TypeError:
            pass
        try:
            return fn(inp), "positional-dict"
        except TypeError as e:
            raise RuntimeError(f"adapter: {e}") from e
    return fn(inp), "positional-scalar"


def main():
    results = {}
    signatures = {}
    total = match = mismatch = error = scenario = 0
    for path in sorted(VEC_DIR.glob("*_api_vectors.json")):
        vectors = json.load(open(path, encoding="utf-8"))
        file_res = []
        for i, v in enumerate(vectors):
            api = v["api"]
            fn = getattr(w, api, None)
            if fn is None:
                # composite scenario ids (e.g. save_load_roundtrip) are covered
                # by dedicated per-language test runners, not the generic driver
                file_res.append({"i": i, "api": api, "status": "SCENARIO-SKIP"})
                scenario += 1
                continue
            if api not in signatures:
                try:
                    signatures[api] = list(inspect.signature(fn).parameters)
                except (TypeError, ValueError):
                    signatures[api] = None
            total += 1
            try:
                result, shape = call(fn, v)
                h = H(result)
            except Exception as e:  # noqa: BLE001
                file_res.append({"i": i, "api": api, "status": "ERROR", "error": f"{type(e).__name__}: {e}"[:200]})
                error += 1
                continue
            committed = H(v["expected"]) if "expected" in v else v.get("det_hash")
            ok = h == committed
            match += ok
            mismatch += not ok
            file_res.append({"i": i, "api": api, "status": "MATCH" if ok else "MISMATCH",
                             "shape": shape, "live_hash": h, "committed_hash": committed})
        results[path.name] = file_res
    summary = {"vector_files": len(results), "vectors_executed": total,
               "match_committed": match, "mismatch_committed": mismatch,
               "errors": error, "scenario_skips": scenario}
    json.dump({"summary": summary, "results": results},
              open("cross_python_results.json", "w", encoding="utf-8"), indent=1)
    json.dump(signatures, open("api_signatures.json", "w", encoding="utf-8"), indent=1)
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
