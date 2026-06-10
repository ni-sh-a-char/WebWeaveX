"""Generate PARITY_MANIFEST.json — the single source of truth for parity state.

Combines:
  * PUBLIC_API_MATRIX.md   (classification + Dart symbol per Python API)
  * tools/_proof_matrix.tsv (strongest proof per Complete API)
  * validation/executable/*_results.json (executed Python/JS/Dart hashes)

Emits one record per Python API:
  {api, python, javascript, dart, contract_parity, behavior_parity,
   executable_parity, classification, proof_type}
"""
import json
import os

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def matrix_rows():
    rows = {}
    for line in open(os.path.join(REPO, "PUBLIC_API_MATRIX.md"), encoding="utf-8"):
        if not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 5:
            continue
        status = cells[-1]
        # Require a status badge emoji to skip header/summary rows.
        if not any(b in status for b in ("✅", "🟡", "⚪", "❌")):
            continue
        name = cells[1].strip("`")
        dart = cells[3].strip("`")
        cls = ("Complete" if "Complete" in status else
               "Partial" if "Partial" in status else
               "Deferred" if "Deferred" in status else "Missing")
        rows[name] = {"dart_symbol": "" if dart == "—" else dart, "classification": cls}
    return rows


def proof_index():
    idx = {}
    p = os.path.join(REPO, "tools", "_proof_matrix.tsv")
    if not os.path.exists(p):
        return idx
    for i, line in enumerate(open(p, encoding="utf-8")):
        if i == 0:
            continue
        parts = line.rstrip("\n").split("\t")
        if len(parts) >= 7:
            idx[parts[0]] = {"proof_type": parts[4], "status": parts[6]}
    return idx


def executable_all3():
    ex = os.path.join(REPO, "validation", "executable")
    try:
        P = {r["id"]: r for r in json.load(open(os.path.join(ex, "python_results.json"), encoding="utf-8"))}
        J = {r["id"]: r for r in json.load(open(os.path.join(ex, "js_results.json"), encoding="utf-8"))}
        D = {r["id"]: r for r in json.load(open(os.path.join(ex, "dart_results.json"), encoding="utf-8"))}
        fixtures = json.load(open(os.path.join(ex, "fixtures.json"), encoding="utf-8"))
    except FileNotFoundError:
        return set()
    apis = {}
    for fx in fixtures:
        apis.setdefault(fx["api"], []).append(fx["id"])
    proven = set()
    for api, ids in apis.items():
        ok = all(
            "hash" in P.get(i, {}) and
            P[i].get("hash") == J.get(i, {}).get("hash") == D.get(i, {}).get("hash")
            for i in ids
        )
        if ok and ids:
            proven.add(api)
    return proven


def main():
    rows = matrix_rows()
    proofs = proof_index()
    exe = executable_all3()

    manifest = []
    for api in sorted(rows):
        r = rows[api]
        cls = r["classification"]
        proof = proofs.get(api, {})
        is_exec = api in exe
        complete = cls == "Complete"
        proof_type = ("EXECUTABLE" if is_exec else
                      proof.get("proof_type", "") if complete else "NONE")
        manifest.append({
            "api": api,
            "python": True,
            "javascript": api not in ("version", "__version__"),
            "dart": bool(r["dart_symbol"]),
            "dart_symbol": r["dart_symbol"],
            "contract_parity": complete,
            "behavior_parity": complete,
            "executable_parity": is_exec,
            "classification": cls,
            "proof_type": proof_type,
        })

    counts = {}
    for m in manifest:
        counts[m["classification"]] = counts.get(m["classification"], 0) + 1

    out = {
        "generated_by": "tools/generate_parity_manifest.py",
        "source_of_truth": "Python 2.0.1 (canonical), JavaScript (reference), Dart",
        "counts": counts,
        "executable_proven_apis": sorted(exe),
        "apis": manifest,
    }
    with open(os.path.join(REPO, "PARITY_MANIFEST.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=2)
        fh.write("\n")
    print("Wrote PARITY_MANIFEST.json")
    print("counts:", counts)
    print("executable-proven:", sorted(exe))


if __name__ == "__main__":
    main()
