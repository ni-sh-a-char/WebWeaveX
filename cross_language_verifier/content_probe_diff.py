import json
import sys
from pathlib import Path

sys.path.insert(0, r"C:\Projects\wwx_cert_py")
from core.extraction.semantic_content_extraction_engine import extract_semantic_content

f = sys.argv[1]
text = (Path("corpus") / f).read_bytes().decode("utf-8", errors="replace")
out = extract_semantic_content(text)
js = json.load(open("probe_js.json", encoding="utf-8"))[f]
for k in sorted(set(out) | set(js)):
    a = json.dumps(out.get(k), ensure_ascii=True, sort_keys=True)
    b = json.dumps(js.get(k), ensure_ascii=True, sort_keys=True)
    print(k, "MATCH" if a == b else "DIFF")
    if a != b and isinstance(out.get(k), list):
        for x, y in zip(out[k], js[k]):
            if x != y:
                print("  py:", json.dumps(x, ensure_ascii=True)[:200])
                print("  js:", json.dumps(y, ensure_ascii=True)[:200])
                break
        if len(out[k]) != len(js[k]):
            print("  len", len(out[k]), len(js[k]))
            pa = [json.dumps(x, ensure_ascii=True) for x in out[k]]
            ja = [json.dumps(x, ensure_ascii=True) for x in js[k]]
            print("  py-only:", [x[:120] for x in pa if x not in ja][:3])
            print("  js-only:", [x[:120] for x in ja if x not in pa][:3])
