"""One-shot generator: append the core.parsers closure fixture set.

Domain note: `language == "python"` fixtures use syntactically INVALID python
(still invalid after recover_syntax paren-repair) so CPython's ast.parse fails
exactly like the certified JS/Dart astModule contract. Valid-python AST
enrichment is a documented Python-only capability outside the parity domain.
"""
import json
import os

D = os.path.dirname(os.path.abspath(__file__))

JS_SRC = (
    "import { api } from './api';\n"
    "class UserService {\n"
    "  constructor() { this.cache = init(); }\n"
    "}\n"
    "function loadUser(id) { return fetchUser(id); }\n"
    "function fetchUser(id) { return api.get(id); }\n"
    "loadUser(1);\n"
)

TS_SRC = (
    "interface Repo { id: string }\n"
    "trait Marker\n"
    "class RepoService {\n"
    "  public string getName() { return name(); }\n"
    "}\n"
    "function syncRepo(r: Repo) { validate(r); persist(r); }\n"
)

GO_SRC = (
    "module example.com/svc\n\n"
    "func handler(w http.ResponseWriter) { render(w) }\n"
    "func render(w io.Writer) { write(w) }\n"
)

BAD_PY = "def broken(:\n    return ]invalid[\nclass Orphan(\n"

PKG_JSON = (
    '{\n  "name": "demo",\n  "dependencies": {"react": "^18.0.0", '
    '"express": "4.18.2"},\n  "devDependencies": {"vitest": "1.0.0"}\n}\n'
)

REQS = "flask==2.3.2\nfastapi>=0.100\nuvicorn\n# pip managed\n"

API_SRC = (
    "@app.get('/users')\n"
    "def list_users(): ...\n"
    "@router.post('/items')\n"
    "def add(): ...\n"
    "GET /health\n"
    "graphql endpoint\n"
)

SYMBOLS_FIXTURE = {
    "classes": ["Svc"], "functions": ["run"], "methods": [],
    "interfaces": [], "traits": [], "imports": ["express", "react"],
    "exports": ["Svc"], "decorators": [], "symbols": ["Svc", "run"],
}

PARSED_FIXTURE = {
    "language": "javascript",
    "source_id": "src/app.js",
    "symbols": SYMBOLS_FIXTURE,
    "imports": {"nodes": ["express", "react", "src/app.js"],
                "edges": [{"from": "src/app.js", "to": "express"},
                          {"from": "src/app.js", "to": "react"}],
                "exports": ["Svc"]},
    "calls": {"calls": [{"from": "<module>", "to": "run"}]},
    "dependencies": {"dependencies": ["express", "react"],
                     "package_managers": ["npm"]},
    "evidence": {"ast": False, "symbols": True, "calls": True,
                 "dependencies": True, "tree_sitter": False,
                 "parse_error": True},
    "semantic_graph": {"nodes": [], "edges": [], "max_edges": 20000},
}

B = []


def fx(i, fn, args):
    B.append({"id": i, "fn": fn, "args": args})


fx("p-detect-js", "parsers.parse_ast", [JS_SRC, "javascript"])
fx("p-ast-py-invalid", "parsers.parse_ast", [BAD_PY, "python"])
fx("p-ast-empty", "parsers.parse_ast", ["", ""])
fx("p-recover-py", "parsers.recover_syntax", ["def f(a, (b\n  x = (1\n", "python"])
fx("p-recover-other", "parsers.recover_syntax", ["fn main( {", "rust"])
fx("p-budget-small", "parsers.enforce_budget", ["tiny source"])
fx("p-symbols-js", "parsers.resolve_symbols", [JS_SRC, "javascript"])
fx("p-symbols-ts", "parsers.resolve_symbols", [TS_SRC, "typescript"])
fx("p-symbols-pybad", "parsers.resolve_symbols", [BAD_PY, "python"])
fx("p-symbols-empty", "parsers.resolve_symbols", ["", "text"])
fx("p-calls-js", "parsers.build_call_graph", [JS_SRC, "javascript"])
fx("p-calls-go", "parsers.build_call_graph", [GO_SRC, "go"])
fx("p-calls-pybad", "parsers.build_call_graph", [BAD_PY, "python"])
fx("p-imports-sym", "parsers.resolve_imports", [SYMBOLS_FIXTURE, "src/app.js"])
fx("p-imports-empty", "parsers.resolve_imports", [{}, "module"])
fx("p-deps-pkgjson", "parsers.resolve_dependencies", [PKG_JSON, "package.json"])
fx("p-deps-reqs", "parsers.resolve_dependencies",
   [REQS, "requirements.txt"])
fx("p-deps-gomod", "parsers.resolve_dependencies",
   ["module example.com/svc\nrequire (\n\texample.com/dep v1.2.3\n)\n",
    "go.mod"])
fx("p-runtime-node", "parsers.resolve_runtime",
   [["react", "express"], ["react-dom"]])
fx("p-runtime-py", "parsers.resolve_runtime",
   [["flask", "fastapi"], ["python_json"]])
fx("p-runtime-empty", "parsers.resolve_runtime", [[], []])
fx("p-frameworks-mixed", "parsers.resolve_frameworks",
   [["django", "react"], ["next/router"], ["route"]])
fx("p-frameworks-empty", "parsers.resolve_frameworks", [[], [], None])
fx("p-api-routes", "parsers.resolve_api_surface", [API_SRC, "python", "app.py"])
fx("p-api-none", "parsers.resolve_api_surface", ["plain text", "text", ""])
fx("p-caps-ts", "parsers.language_capabilities", ["typescript"])
fx("p-caps-unknown", "parsers.language_capabilities", ["cobol"])
fx("p-graph-parsed", "parsers.build_semantic_graph", [PARSED_FIXTURE])
fx("p-graph-empty", "parsers.build_semantic_graph", [{}])
fx("p-cognition-parsed", "parsers.build_parser_cognition_evidence",
   [PARSED_FIXTURE])
fx("p-cognition-nondict", "parsers.build_parser_cognition_evidence",
   ["notadict"])
fx("p-grounding-parsed", "ground_parser_output", [PARSED_FIXTURE])
fx("p-grounding-nondict", "ground_parser_output", ["notadict"])
fx("p-normalize-parsed", "parsers.normalize_parser_output", [PARSED_FIXTURE])
fx("p-require-parsed", "parsers.require_parser_evidence", [PARSED_FIXTURE])
fx("p-require-text", "parsers.require_parser_evidence",
   [{"language": "text", "symbols": {}}])
fx("p-source-js", "parsers.parse_source", [JS_SRC, "src/app.js"])
fx("p-source-ts-hint", "parsers.parse_source", [TS_SRC, "", "typescript"])
fx("p-source-pybad", "parsers.parse_source", [BAD_PY, "broken.py"])
fx("p-source-pkgjson", "parsers.parse_source", [PKG_JSON, "package.json"])
fx("p-source-empty", "parsers.parse_source", ["", ""])
fx("p-stream-2chunks", "parsers.stream_parse",
   [GO_SRC + "\n" + GO_SRC, "svc/go.mod", "", 3])
fx("p-repoanalyze-js", "parsers.analyze_repository_source",
   [JS_SRC, "src/app.js"])

path = os.path.join(D, "fixtures.json")
existing = json.load(open(path, encoding="utf-8-sig"))
ids = {f["id"] for f in existing}
assert not ids & {f["id"] for f in B}
merged = existing + B
with open(path, "w", encoding="utf-8") as fh:
    json.dump(merged, fh, ensure_ascii=False, indent=1)
print(f"added {len(B)} parser fixtures -> {len(merged)} total")
