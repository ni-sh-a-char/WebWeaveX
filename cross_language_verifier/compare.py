"""Cross-language verifier — comparator.

Reads out_python.json / out_js.json / out_dart.json (3 runs each when present),
verifies per-language determinism and cross-language byte equality per field,
and writes parity_report.json, failure_vectors.json, certification_report.json.
"""
import json
import hashlib
import sys

FIELDS = ["stable", "canonical", "hash", "encrypted_b64", "roundtrip_ok", "fingerprint_hex"]
LANGS = ["python", "js", "dart"]


def load(path):
    with open(path, "rb") as f:
        data = f.read()
    if data[:2] in (b"\xff\xfe", b"\xfe\xff"):
        return json.loads(data.decode("utf-16"))
    return json.loads(data.decode("utf-8-sig"))


def first_diff(a, b):
    ab, bb = a.encode("utf-8"), b.encode("utf-8")
    n = min(len(ab), len(bb))
    for i in range(n):
        if ab[i] != bb[i]:
            return {"byte_offset": i, "python": f"0x{ab[i]:02x}", "other": f"0x{bb[i]:02x}"}
    return {"byte_offset": n, "note": f"length {len(ab)} vs {len(bb)}"}


def main():
    runs = {}
    determinism = {}
    for lang in LANGS:
        outs = [load(f"out_{lang}_{i}.json") for i in (1, 2, 3)]
        hashes = [hashlib.sha256(json.dumps(o, sort_keys=True, ensure_ascii=True).encode()).hexdigest() for o in outs]
        determinism[lang] = {"identical_runs": len(set(hashes)) == 1, "run_digests": hashes}
        runs[lang] = outs[0]

    failures = []
    matched = 0
    total = 0
    vids = sorted(runs["python"]["vectors"].keys())

    if not (runs["python"]["time_key"] == runs["js"]["time_key"] == runs["dart"]["time_key"]):
        failures.append({"vector": "<time_key>", "field": "time_key",
                         "values": {l: runs[l]["time_key"] for l in LANGS}})
    else:
        matched += 1
    total += 1

    for vid in vids:
        for f in FIELDS:
            total += 1
            vals = {l: runs[l]["vectors"].get(vid, {}).get(f) for l in LANGS}
            uniq = {json.dumps(v, ensure_ascii=True, sort_keys=True) for v in vals.values()}
            if len(uniq) == 1:
                matched += 1
                continue
            entry = {"vector": vid, "field": f, "values": {l: (v if isinstance(v, (bool, type(None))) else str(v)[:300]) for l, v in vals.items()}}
            pv = vals["python"]
            if isinstance(pv, str):
                for l in ("js", "dart"):
                    if isinstance(vals[l], str) and vals[l] != pv:
                        entry[f"first_diff_python_vs_{l}"] = first_diff(pv, vals[l])
            failures.append(entry)

    roundtrip_fail = [vid for vid in vids for l in LANGS
                      if runs[l]["vectors"].get(vid, {}).get("roundtrip_ok") is not True]

    all_deterministic = all(d["identical_runs"] for d in determinism.values())
    parity_pass = not failures and not roundtrip_fail

    parity_report = {
        "vectors_total": len(vids),
        "fields_compared": total,
        "fields_matched": matched,
        "fields_mismatched": len(failures),
        "roundtrip_failures": sorted(set(roundtrip_fail)),
        "determinism": determinism,
        "languages": {"python": "branch python @ core/", "javascript": "branch javascript @ src/", "dart": "branch dart @ lib/"},
    }
    with open("parity_report.json", "w", encoding="utf-8") as f:
        json.dump(parity_report, f, indent=1, ensure_ascii=False)
    with open("failure_vectors.json", "w", encoding="utf-8") as f:
        json.dump(failures, f, indent=1, ensure_ascii=False)

    certification = {
        "verdict": "PASS" if (parity_pass and all_deterministic) else "FAIL",
        "claim": "Python == JavaScript == Dart, byte-identical, for all deterministic vectors",
        "vectors": len(vids),
        "fields_compared": total,
        "byte_identical_fields": matched,
        "per_language_determinism_3_runs": all_deterministic,
        "encryption_roundtrip_all_pass": not roundtrip_fail,
        "input_domain_contract": [
            "integers: |n| <= 2^53",
            "floats: IEEE-754 doubles; integral floats < 2^63 canonicalize to integers; non-finite -> null",
            "strings: Unicode scalar sequences (no lone surrogates); NFKC applied to top-level strings only",
        ],
    }
    with open("certification_report.json", "w", encoding="utf-8") as f:
        json.dump(certification, f, indent=1, ensure_ascii=False)

    print(json.dumps(certification, indent=1))
    if failures[:8]:
        print("\nFIRST FAILURES:")
        print(json.dumps(failures[:8], indent=1, ensure_ascii=False))
    sys.exit(0 if certification["verdict"] == "PASS" else 1)


if __name__ == "__main__":
    main()
