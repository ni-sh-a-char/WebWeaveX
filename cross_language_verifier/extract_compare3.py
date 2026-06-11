"""Three-way extraction comparator: Python vs JavaScript vs Dart."""
import json
import sys


def load(p):
    raw = open(p, "rb").read()
    if raw[:2] in (b"\xff\xfe", b"\xfe\xff"):
        return json.loads(raw.decode("utf-16"))
    return json.loads(raw.decode("utf-8-sig"))


py = load("extract_py_out.json")
js = load("extract_js_out.json")
da = load("extract_dart_out.json")

result = {"torture": {"total": 0, "match": 0, "fail": []},
          "corpus": {"total": 0, "match": 0, "fail": []}}

for section in ("torture", "corpus"):
    keys = sorted(set(py[section]) | set(js[section]) | set(da[section]))
    for k in keys:
        result[section]["total"] += 1
        a, b, c = py[section].get(k, {}), js[section].get(k, {}), da[section].get(k, {})
        hm = a.get("html_hash") == b.get("html_hash") == c.get("html_hash") and a.get("html_hash")
        cm = a.get("content_hash") == b.get("content_hash") == c.get("content_hash") and a.get("content_hash")
        if hm and cm:
            result[section]["match"] += 1
        else:
            entry = {"id": k,
                     "html": {"py": a.get("html_hash", "")[:12], "js": b.get("html_hash", "")[:12], "dart": c.get("html_hash", "")[:12]},
                     "content": {"py": a.get("content_hash", "")[:12], "js": b.get("content_hash", "")[:12], "dart": c.get("content_hash", "")[:12]}}
            if section == "torture":
                entry["py_out"] = a.get("html_out")
                entry["dart_out"] = c.get("html_out")
            result[section]["fail"].append(entry)

verdict = "PASS" if not result["torture"]["fail"] and not result["corpus"]["fail"] else "FAIL"
summary = {"torture": f"{result['torture']['match']}/{result['torture']['total']}",
           "corpus": f"{result['corpus']['match']}/{result['corpus']['total']}",
           "verdict": verdict}
print(json.dumps(summary, indent=1))
fails = result["torture"]["fail"] + result["corpus"]["fail"]
json.dump(result, open("extract3_detail.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
if fails:
    print("first fails:", json.dumps([{kk: vv for kk, vv in f.items() if kk in ("id", "html", "content")} for f in fails[:8]], indent=1))
sys.exit(0 if verdict == "PASS" else 1)
