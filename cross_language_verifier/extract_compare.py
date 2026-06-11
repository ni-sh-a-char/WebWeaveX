"""Phase 10/11 comparator: Python vs JavaScript extraction over identical bytes.
Dart: no HTML semantic extraction engine exists — documented blocker."""
import json


def load(p):
    raw = open(p, "rb").read()
    if raw[:2] in (b"\xff\xfe", b"\xfe\xff"):
        return json.loads(raw.decode("utf-16"))
    return json.loads(raw.decode("utf-8-sig"))


py = load("extract_py_out.json")
js = load("extract_js_out.json")

report = {"torture": {"total": 0, "match": 0, "fail": []},
          "corpus": {"total": 0, "match": 0, "fail": []}}

for tid in sorted(set(py["torture"]) | set(js["torture"])):
    report["torture"]["total"] += 1
    a, b = py["torture"].get(tid, {}), js["torture"].get(tid, {})
    if a.get("html_hash") == b.get("html_hash") and a.get("content_hash") == b.get("content_hash"):
        report["torture"]["match"] += 1
    else:
        report["torture"]["fail"].append({
            "id": tid,
            "html_match": a.get("html_hash") == b.get("html_hash"),
            "content_match": a.get("content_hash") == b.get("content_hash"),
            "py_html_out": a.get("html_out"), "js_html_out": b.get("html_out"),
        })

for f in sorted(set(py["corpus"]) | set(js["corpus"])):
    report["corpus"]["total"] += 1
    a, b = py["corpus"].get(f, {}), js["corpus"].get(f, {})
    if a.get("html_hash") == b.get("html_hash") and a.get("content_hash") == b.get("content_hash"):
        report["corpus"]["match"] += 1
    else:
        report["corpus"]["fail"].append({"file": f,
                                         "html_match": a.get("html_hash") == b.get("html_hash"),
                                         "content_match": a.get("content_hash") == b.get("content_hash")})

verdict = "PASS" if not report["torture"]["fail"] and not report["corpus"]["fail"] else "FAIL"
out = {
    "scope": "extract_semantic_html + extract_semantic_content, Python (bs4 html.parser) vs JavaScript (PySoup port), identical input bytes",
    "dart": "FAIL-BY-ABSENCE: no HTML semantic extraction engine implemented (documented blocker; 22 extraction-family APIs unexported in Dart)",
    "torture_cases": {"total": report["torture"]["total"], "match": report["torture"]["match"]},
    "real_pages": {"total": report["corpus"]["total"], "match": report["corpus"]["match"]},
    "python_vs_js_verdict": verdict,
    "failures": {"torture": [
        {k: v for k, v in x.items() if k != "py_html_out" and k != "js_html_out"} for x in report["torture"]["fail"]
    ], "corpus": report["corpus"]["fail"][:30]},
}
json.dump(out, open("extraction_certification.json", "w", encoding="utf-8"), indent=1)
json.dump(report["torture"]["fail"], open("extraction_torture_fail_detail.json", "w", encoding="utf-8"),
          indent=1, ensure_ascii=False)
print(json.dumps({k: out[k] for k in ("torture_cases", "real_pages", "python_vs_js_verdict")}, indent=1))
