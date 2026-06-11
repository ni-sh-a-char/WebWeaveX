import json
import sys
from pathlib import Path

sys.path.insert(0, r"C:\Projects\wwx_cert_py")
from core.extraction.semantic_content_extraction_engine import extract_semantic_content

f = sys.argv[1]
text = (Path("corpus") / f).read_bytes().decode("utf-8", errors="replace")
out = extract_semantic_content(text)
with open("probe_py.json", "wb") as fh:
    fh.write(json.dumps({f: out}, ensure_ascii=False, sort_keys=True, indent=1).encode("utf-8"))
print("py fields:", {k: len(v) if isinstance(v, list) else v for k, v in out.items()})
