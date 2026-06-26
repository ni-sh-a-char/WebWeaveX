#!/usr/bin/env python3
"""Session-34 parser-engine golden vectors from canonical Python 2.1.0 (text-path regex engines).

Certifies the Java parser foundation (io.webweavex.repository.ParserEngines) byte-exact against the
canonical Python parser sub-engines that feed compile_repository_ir's observable output. Text path
(language detection by extension; source-only inputs are language="text" → regex engines).
"""
from __future__ import annotations

import json
import sys

from core.crypto.kaalka_hash_engine import compute_kaalka_hash
from core.determinism.normalization import stable_serialize
from core.parsers.symbol_resolution_engine import resolve_symbols
from core.parsers.call_graph_engine import build_call_graph
from core.parsers.dependency_resolution_engine import resolve_dependencies
from core.parsers.runtime_resolution_engine import resolve_runtime
from core.parsers.import_resolution_engine import resolve_imports
from core.parsers.framework_resolution_engine import resolve_frameworks
from core.parsers.syntax_recovery_engine import recover_syntax
from core.parsers.parser_budget_engine import enforce_budget

SRCS = {
    "py_simple": "import os\ndef main():\n    helper()\n    return 1\ndef helper():\n    pass\n",
    "py_class": "class Foo(Base):\n    def m(self):\n        return self.x\nclass Bar:\n    pass\n",
    "empty": "",
    "reqs": "flask==2.0\nrequests>=2.0\nnumpy\n",
    "prose": "this is not code\njust some words here\n",
    "js_like": "function handler(req) {\n  return doWork(req);\n}\nconst x = 1;\n",
}
DEPS_SRCS = {
    "reqs": "flask==2.0\nrequests>=2.0\nnumpy\n",
    "pkgjson": '{"dependencies": {"react": "^18", "next": "13"}, "devDependencies": {"vitest": "1"}}',
    "cargo": "[dependencies]\ntokio = \"1.0\"\nactix-web = \"4\"\n",
    "empty": "",
    "py": "import os\ndef main():\n    pass\n",
}


def ev(name, inputs, value):
    return {"name": name, "inputs": inputs,
            "serialized": stable_serialize(value), "hash": compute_kaalka_hash(value)}


def main() -> None:
    out = {"source": "Python 2.1.0 canonical (session 34: parser engines, text path)"}
    out["resolve_symbols"] = [ev(n, {"source": s}, resolve_symbols(s, "text")) for n, s in SRCS.items()]
    out["build_call_graph"] = [ev(n, {"source": s}, build_call_graph(s, "text")) for n, s in SRCS.items()]
    out["resolve_dependencies"] = [ev(n, {"source": s}, resolve_dependencies(s, "")) for n, s in DEPS_SRCS.items()]
    out["recover_syntax"] = [
        ev("py_unbalanced", {"source": "def f(\n    return 1\n", "language": "python"},
           recover_syntax("def f(\n    return 1\n", "python")),
        ev("text", {"source": "a b c", "language": "text"}, recover_syntax("a b c", "text")),
    ]
    out["enforce_budget"] = [ev("small", {"source": "abc"}, enforce_budget("abc", None))]
    # runtime/imports/frameworks: feed from resolved symbols/deps
    SYM = resolve_symbols(SRCS["py_simple"], "text")
    out["resolve_imports"] = [ev("py_simple", {"symbols": SYM}, resolve_imports(SYM, "mod"))]
    out["resolve_runtime"] = [
        ev("flask", {"deps": ["flask", "uvicorn"], "imports": ["flask"]}, resolve_runtime(["flask", "uvicorn"], ["flask"])),
        ev("empty", {"deps": [], "imports": []}, resolve_runtime([], [])),
    ]
    out["resolve_frameworks"] = [
        ev("react", {"deps": ["react", "next"], "imports": ["react"]}, resolve_frameworks(["react", "next"], ["react"], [])),
        ev("empty", {"deps": [], "imports": []}, resolve_frameworks([], [], [])),
    ]
    path = sys.argv[1] if len(sys.argv) > 1 else "parser_vectors_s34.json"
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2)
    total = sum(len(v) for k, v in out.items() if isinstance(v, list))
    print(f"wrote {path} ({total} vectors)")


if __name__ == "__main__":
    main()
