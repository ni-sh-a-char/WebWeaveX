"""Proof Coverage Audit: for every COMPLETE API, locate Python/JS/Dart sources
and the strongest available proof. Emits tools/_proof_matrix.tsv.

Proof precedence (strongest first):
  VECTOR        - python_name appears as an `api`/`id` in a validation/parity vector json
  CORE_VECTOR   - covered by the 11-case three-way crypto vectors (hash/encrypt/decrypt)
  PARITY_TEST   - dart symbol asserted in test/parity/*.dart
  ROUNDTRIP     - dart symbol in a save/load deep-equality roundtrip test
  TEST_ONLY     - dart symbol referenced only in a determinism/structural test (WEAK)
  NONE          - no executed reference (FAIL)
"""
import json
import os
import re
import subprocess

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MATRIX = os.path.join(REPO, "PUBLIC_API_MATRIX.md")

CORE_CRYPTO = {"encrypt_value", "decrypt_value", "compute_kaalka_hash"}


def git_grep_file(ref, pattern, pathspec=None):
    cmd = ["git", "-C", REPO, "grep", "-l", "-E", pattern, ref]
    if pathspec:
        cmd += ["--", pathspec]
    try:
        out = subprocess.check_output(cmd, stderr=subprocess.DEVNULL).decode()
        # strip "ref:" prefix
        files = [l.split(":", 1)[1] for l in out.strip().splitlines() if ":" in l]
        return files[0] if files else ""
    except subprocess.CalledProcessError:
        return ""


def complete_rows():
    rows = []
    for line in open(MATRIX, encoding="utf-8"):
        if "Complete" not in line or not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 5 or "Complete" not in cells[-1]:
            continue
        rows.append((cells[1].strip("`"), cells[3].strip("`")))
    return rows


def vector_apis():
    """map api/id -> vector file."""
    apis = {}
    vdir = os.path.join(REPO, "validation", "parity")
    for fn in os.listdir(vdir):
        if not fn.endswith(".json"):
            continue
        try:
            data = json.load(open(os.path.join(vdir, fn), encoding="utf-8-sig"))
        except Exception:
            continue
        items = data if isinstance(data, list) else data.get("vectors", [])
        for it in items:
            if not isinstance(it, dict):
                continue
            for key in ("api", "id"):
                if key in it:
                    apis.setdefault(str(it[key]), fn)
    return apis


def test_index():
    """symbol -> list of (file, is_parity, is_roundtrip)."""
    refs = {}
    tdir = os.path.join(REPO, "test")
    files = {}
    for root, _, fns in os.walk(tdir):
        for fn in fns:
            if fn.endswith(".dart"):
                p = os.path.join(root, fn)
                files[p] = open(p, encoding="utf-8", errors="replace").read()
    return files


def main():
    rows = complete_rows()
    vapis = vector_apis()
    tfiles = test_index()

    out = []
    weak = []
    for pyname, dart in rows:
        sym = dart.split(".")[0] if dart else ""
        # sources
        py_pat = (r"^\s*(async\s+)?def\s+%s\b|^\s*class\s+%s\b|^\s*%s\s*[:=]"
                  % (re.escape(pyname), re.escape(pyname), re.escape(pyname)))
        py_src = git_grep_file("origin/python", py_pat, "core") \
            or git_grep_file("origin/python", py_pat, "webweavex") \
            or git_grep_file("origin/python", py_pat)
        js_pat = r"\b%s\b" % re.escape(sym) if sym else re.escape(pyname)
        js_src = git_grep_file("origin/javascript",
                               r"export[^\n]*\b%s\b|function\s+%s\b|const\s+%s\b"
                               % (re.escape(sym), re.escape(sym), re.escape(sym)),
                               "src") if sym else ""
        dart_src = ""
        for root, _, fns in os.walk(os.path.join(REPO, "lib")):
            for fn in fns:
                if not fn.endswith(".dart"):
                    continue
                p = os.path.join(root, fn)
                txt = open(p, encoding="utf-8", errors="replace").read()
                if re.search(r"[A-Za-z<>,\s]+\s%s\s*\(" % re.escape(sym), txt) or \
                   re.search(r"\bclass\s+%s\b" % re.escape(sym), txt):
                    dart_src = os.path.relpath(p, REPO).replace("\\", "/")
                    break
            if dart_src:
                break

        # proof (strict)
        proof_type, proof_loc = "NONE", ""
        method_vec = next((v for v in vapis if v.startswith(pyname + ".")), None)
        if pyname in vapis:
            proof_type, proof_loc = "VECTOR", "validation/parity/" + vapis[pyname]
        elif method_vec:
            proof_type, proof_loc = ("VECTOR",
                                     "validation/parity/" + vapis[method_vec]
                                     + f" ({method_vec})")
        elif pyname in CORE_CRYPTO:
            proof_type = "CORE_VECTOR"
            proof_loc = "validation/parity/{dart,js,python}_vectors.json"
        elif pyname == "build_runtime_graph":
            # proven cross-language via the core 'graph' vector case in
            # validate_parity.dart (payload = buildRuntimeGraph(...).toJson()).
            proof_type = "CORE_VECTOR"
            proof_loc = "validation/parity/{dart,js,python}_vectors.json (graph case)"
        elif pyname.startswith("save_") or pyname.startswith("load_"):
            # save/load pairs are proven by a save->load->deep-equality roundtrip.
            base = None
            for p, txt in tfiles.items():
                if re.search(r"\b%s\b" % re.escape(sym), txt) and \
                   re.search(r"equals\(|_canonical\(|computeDeterministicHash\(",
                             txt):
                    base = os.path.relpath(p, REPO).replace("\\", "/")
                    if "parity" in base:
                        break
            if base:
                proof_type, proof_loc = "ROUNDTRIP", base
            else:
                proof_type = "TEST_ONLY"
        else:
            # require the symbol to be the SUBJECT of a parity-vector assertion;
            # mere presence in a test = TEST_ONLY (weak).
            test_file = ""
            for p, txt in tfiles.items():
                if sym and re.search(r"\b%s\b" % re.escape(sym), txt):
                    test_file = os.path.relpath(p, REPO).replace("\\", "/")
                    break
            proof_type = "TEST_ONLY" if test_file else "NONE"
            proof_loc = test_file

        status = "PROVEN" if proof_type in (
            "VECTOR", "CORE_VECTOR", "PARITY_TEST", "ROUNDTRIP") else (
            "WEAK" if proof_type == "TEST_ONLY" else "UNPROVEN")
        if status != "PROVEN":
            weak.append((pyname, dart, proof_type))
        out.append((pyname, py_src, js_src, dart_src, proof_type, proof_loc, status))

    with open(os.path.join(REPO, "tools", "_proof_matrix.tsv"), "w",
              encoding="utf-8") as fh:
        fh.write("api\tpy\tjs\tdart\tproof_type\tproof_loc\tstatus\n")
        for r in out:
            fh.write("\t".join(r) + "\n")

    print(f"COMPLETE APIs audited: {len(out)}")
    from collections import Counter
    print("Proof types:", dict(Counter(r[4] for r in out)))
    print("Statuses:", dict(Counter(r[6] for r in out)))
    print(f"\nNON-PROVEN ({len(weak)}):")
    for n, d, pt in weak:
        print(f"  {n}  ->  {d}   [{pt}]")


if __name__ == "__main__":
    main()
