"""Real-world scenario runner (Python). Feeds REAL artifacts — this repo's
own README, a real TypeScript engine source, a real corpus page — through the
public dispatchers and emits canonical hashes.

Usage: PYTHONPATH=<py-clone> python real_world_py.py <dart_clone_dir> <js_clone_dir>
"""
import io
import json
import sys

import webweavex
from core.crypto.kaalka_hash_engine import compute_kaalka_hash as H

DART = sys.argv[1]
JS = sys.argv[2]


def read(p):
    # newline='' preserves CRLF: universal-newline collapsing would shift
    # code-point caps relative to Dart/JS readers
    return io.open(p, encoding='utf-8', errors='replace', newline='').read()


readme = read(f"{DART}/README.md")
ts_src = read(f"{JS}/src/parsers/parserRegistry.ts")
page = read(f"{DART}/cross_language_verifier/corpus/page_0000.html")

out = {}
out["doc_readme"] = H(webweavex.compile_document(readme[:20000]))
out["query_doc_readme"] = H(webweavex.query_documents(text=readme[:20000]))
out["repo_ts_engine"] = H(webweavex.compile_repository(
    ts_src, path="src/parsers/parserRegistry.ts"))
out["query_repo_ts"] = H(webweavex.query_repository(
    source=ts_src, path="src/parsers/parserRegistry.ts"))
out["reason_discourse"] = H(webweavex.reason_semantically(
    "discourse", {"text": readme[:5000]}))
out["reason_runtime"] = H(webweavex.reason_semantically(
    "runtime", {"source": ts_src, "path": "src/parsers/parserRegistry.ts"}))
out["app_cognition_real_page"] = H(webweavex.run_application_cognition(
    "https://release.test/app", page))
out["semantics_repo"] = H(webweavex.query_semantics(
    "repository", {"source": ts_src, "path": "x.ts"}))
print(json.dumps(out, sort_keys=True))
