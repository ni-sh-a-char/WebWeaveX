"""Dump full Python extraction output for selected corpus pages."""
import json
import sys
from pathlib import Path

sys.path.insert(0, r"C:\Projects\wwx_cert_py")
from core.browser.html_semantic_extraction_engine import extract_semantic_html

files = sys.argv[1:]
out = {}
for f in files:
    text = (Path("corpus") / f).read_bytes().decode("utf-8", errors="replace")
    out[f] = extract_semantic_html(text)
with open("probe_py.json", "wb") as fh:
    fh.write(json.dumps(out, ensure_ascii=False, sort_keys=True, indent=1).encode("utf-8"))
print("written", files)
