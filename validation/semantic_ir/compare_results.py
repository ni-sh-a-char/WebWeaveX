"""Compare the three executed result sets (Python canonical, JS, Dart).

Enforces, per fixture id:
  1. hash equality:  hash(Python) == hash(JS) == hash(Dart)
  2. deep value equality of outputs (Python's == — int/float numeric equality;
     float TYPE parity is carried by the hash, whose canonical payload formats
     floats Python-style, e.g. 0.0 -> "0.0").

Exit 0 only if every fixture passes in all three languages.
Usage: python compare_results.py <dir with python_results.json js_results.json dart_results.json>
"""
import json
import os
import sys


def load(d, name):
    with open(os.path.join(d, name), encoding="utf-8-sig") as fh:
        return {r["id"]: r for r in json.load(fh)}


def main():
    d = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
    py = load(d, "python_results.json")
    js = load(d, "js_results.json")
    dart = load(d, "dart_results.json")
    if set(py) != set(js) or set(py) != set(dart):
        print(f"FIXTURE SET MISMATCH: py={len(py)} js={len(js)} dart={len(dart)}")
        sys.exit(1)
    failures = 0
    for fid in py:
        p, j, dt = py[fid], js[fid], dart[fid]
        errs = [name for name, r in (("py", p), ("js", j), ("dart", dt)) if "error" in r]
        if errs:
            print(f"FAIL {fid}: errors in {errs}: "
                  f"{[r.get('error') for r in (p, j, dt) if 'error' in r]}")
            failures += 1
            continue
        if not (p["hash"] == j["hash"] == dt["hash"]):
            print(f"FAIL {fid} [{p['fn']}] hash: py={p['hash'][:12]} "
                  f"js={j['hash'][:12]} dart={dt['hash'][:12]}")
            failures += 1
            continue
        if not (p["output"] == j["output"] == dt["output"]):
            print(f"FAIL {fid} [{p['fn']}] deep-equality mismatch")
            failures += 1
            continue
    total = len(py)
    if failures:
        print(f"RESULT: {total - failures}/{total} fixtures pass — PARITY NOT PROVEN")
        sys.exit(1)
    print(f"RESULT: {total}/{total} fixtures pass — Python == JavaScript == Dart "
          f"(hash + deep equality)")


if __name__ == "__main__":
    main()
