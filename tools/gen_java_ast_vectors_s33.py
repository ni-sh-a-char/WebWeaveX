#!/usr/bin/env python3
"""Session-33 AST-subsystem golden vectors from canonical Python 2.1.0 (real `ast`).

Certifies the Java AST scanner (io.webweavex.ast.PythonAstEngine / SemanticAstIr, ported from the
certified JS scanner) byte-exact against CPython's real `ast.walk` summary for standard source.
"""
from __future__ import annotations

import json
import sys

from core.crypto.kaalka_hash_engine import compute_kaalka_hash
from core.determinism.normalization import stable_serialize
from core.ast.python_ast_engine import parse_python_ast
from core.ast.semantic_ast_ir_engine import compile_semantic_ast_ir

SOURCES = {
    "empty": "",
    "simple": "import os\ndef foo(a, b):\n    x = bar()\n    return x\nclass A(Base):\n    pass\n",
    "mixed": (
        "import os\n"
        "from a.b import c, d as e\n"
        "def foo(a, b=2, *args):\n"
        "    x = bar()\n"
        "    return x\n"
        "def baz():\n"
        "    pass\n"
        "class A(Base):\n"
        "    def m(self):\n"
        "        return 1\n"
        "y = 5\n"
    ),
    "imports": "import os, sys\nimport json as j\nfrom typing import Any, Dict, List\n",
    "nested": (
        "def outer(p):\n"
        "    def inner(q):\n"
        "        z = q\n"
        "        return z\n"
        "    return inner\n"
        "class C:\n"
        "    def a(self):\n"
        "        pass\n"
        "    def b(self):\n"
        "        pass\n"
    ),
    "multiline_sig": "def long(\n    a,\n    b,\n    c,\n):\n    return a\n",
    "assignments": "a = 1\nb, c = 2, 3\nd = a + b\nclass K:\n    e = 5\n",
}


def ev(name, code, value):
    return {"name": name, "code": code,
            "serialized": stable_serialize(value), "hash": compute_kaalka_hash(value)}


def main() -> None:
    out = {"source": "Python 2.1.0 canonical (session 33: AST subsystem, real ast.walk)"}
    out["parse_python_ast"] = [ev(n, c, parse_python_ast(c)) for n, c in SOURCES.items()]
    out["compile_semantic_ast_ir"] = [ev(n, c, compile_semantic_ast_ir(c)) for n, c in SOURCES.items()]
    path = sys.argv[1] if len(sys.argv) > 1 else "ast_vectors_s33.json"
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2)
    total = sum(len(v) for k, v in out.items() if isinstance(v, list))
    print(f"wrote {path} ({total} vectors)")


if __name__ == "__main__":
    main()
