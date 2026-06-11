"""Phase 12: compare live semantic-IR runs across Python/JS/Dart.

Single hashing authority: the comparator itself recomputes the canonical hash
(updated Python compute_kaalka_hash) over each language's raw `output`, so
per-runner hash shims cannot mask or fabricate (mis)matches.
"""
import json
import sys

sys.path.insert(0, r"C:\Projects\wwx_cert_py")
from core.crypto.kaalka_hash_engine import compute_kaalka_hash as H


def load(p):
    raw = open(p, "rb").read()
    if raw[:2] in (b"\xff\xfe", b"\xfe\xff"):
        return json.loads(raw.decode("utf-16"))
    return json.loads(raw.decode("utf-8-sig"))


py = load("sir_python.json")
js = load("sir_js.json")
da = load("sir_dart.json")

by_id = lambda rows: {r["id"]: r for r in rows}
P, J, D = by_id(py), by_id(js), by_id(da)
ids = sorted(set(P) | set(J) | set(D))
match = 0
fails = []
for i in ids:
    rp, rj, rd = P.get(i, {}), J.get(i, {}), D.get(i, {})
    if any(r.get("error") for r in (rp, rj, rd)) or not all("output" in r for r in (rp, rj, rd)):
        fails.append({"id": i, "py_err": rp.get("error"), "js_err": rj.get("error"),
                      "dart_err": rd.get("error")})
        continue
    hp, hj, hd = H(rp["output"]), H(rj["output"]), H(rd["output"])
    if hp == hj == hd:
        match += 1
    else:
        fails.append({"id": i, "python": hp, "js": hj, "dart": hd})
report = {"fixtures": len(ids), "hash_match_3way": match, "mismatches": len(fails),
          "verdict": "PASS" if not fails else "FAIL", "failures": fails[:20]}
json.dump(report, open("semantic_ir_certification.json", "w", encoding="utf-8"), indent=1)
print(json.dumps({k: report[k] for k in ("fixtures", "hash_match_3way", "mismatches", "verdict")}, indent=1))
if fails:
    print(json.dumps(fails[:6], indent=1)[:1500])
