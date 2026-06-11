import json
import sys

sys.path.insert(0, r"C:\Projects\wwx_cert_py")
from core.browser.html_semantic_extraction_engine import extract_semantic_html
from core.extraction.semantic_content_extraction_engine import extract_semantic_content
from core.crypto.kaalka_hash_engine import compute_kaalka_hash as H

vectors = json.load(open(sys.argv[1], encoding="utf-8"))
out = {vid: {"h": H(extract_semantic_html(html)), "c": H(extract_semantic_content(html))}
       for vid, html in vectors.items()}
with open(sys.argv[2], "wb") as f:
    f.write(json.dumps(out, sort_keys=True).encode("utf-8"))
print(f"python synth: {len(out)}")
