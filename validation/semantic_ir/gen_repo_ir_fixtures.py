"""One-shot generator: append the repository-IR closure fixture set.

Domain: dispatcher fixtures (compile_repository_ir / query_repository /
reason_runtime_semantic) use sources where Python's ast.parse and the
certified scanner BOTH fail (empty source, or first logical line starting
with '<' as in JSX/Vue), keeping compile_semantic_ast_ir on the shared
fallback path. Non-dispatcher engines accept any non-python source.
"""
import json
import os

D = os.path.dirname(os.path.abspath(__file__))

JS_SVC = (
    "import { db } from './db';\n"
    "class OrderService {\n"
    "  create(order) { return persist(order); }\n"
    "}\n"
    "function persist(o) { return db.save(o); }\n"
    "function notify(o) { publish(o); }\n"
    "persist(notify({}));\n"
)

JSX_APP = (
    "<template>\n"
    "  <div class='app'>{render()}</div>\n"
    "</template>\n"
    "function render() { return view(); }\n"
    "function view() { return fetchData(); }\n"
)

GO_SVC = (
    "func main() { serve() }\n"
    "func serve() { listen() }\n"
)

FILES = ["src\\Dockerfile", "k8s/deploy.yaml", "services/order.js",
         "services/billing.js", ".github/workflows/ci.yml"]

OPENAPI = {"paths": {"/orders": {"get": {}, "post": {}},
                     "/health": {"delete": {}}}}

B = []


def fx(i, fn, args):
    B.append({"id": i, "fn": fn, "args": args})


fx("r-semir-js", "build_repository_semantic_ir", [JS_SVC, "services/order.js", FILES])
fx("r-semir-empty", "build_repository_semantic_ir", ["", "", None])
fx("r-execdeps-js", "model_execution_dependencies", [JS_SVC, "services/order.js"])
fx("r-execdeps-go", "model_execution_dependencies", [GO_SVC, "main.go"])
fx("r-execdeps-empty", "model_execution_dependencies", ["", ""])
fx("r-runtsem-js", "analyze_runtime_semantics", [JS_SVC, "services/order.js"])
fx("r-runtsem-empty", "analyze_runtime_semantics", ["", ""])
fx("r-svcgraph-js", "build_service_runtime_graph",
   [JS_SVC, "services/order.js", FILES])
fx("r-svcgraph-empty", "build_service_runtime_graph", ["", "", []])
fx("r-runtexec-js", "analyze_runtime_execution", [JS_SVC, "services/order.js"])
fx("r-runtflow-js", "reason_runtime_flow", [JS_SVC, "services/order.js", FILES])
fx("r-execir-js", "build_repository_execution_ir",
   [JS_SVC, "services/order.js", FILES, OPENAPI])
fx("r-execir-noapi", "build_repository_execution_ir",
   [GO_SVC, "main.go", FILES, None])
fx("r-state-js", "model_runtime_state", [JS_SVC, "services/order.js"])
fx("r-state-empty", "model_runtime_state", ["", ""])
# dispatchers — shared-fallback semantic_ast domain
fx("r-compile-empty", "compile_repository_ir", ["", "", None, None])
fx("r-compile-jsx", "compile_repository_ir",
   [JSX_APP, "src/App.jsx", FILES, OPENAPI])
fx("r-query-jsx", "query_repository", [JSX_APP, "src/App.jsx", FILES])
fx("r-query-empty", "query_repository", ["", "", None])
fx("r-reason-jsx", "reason_runtime_semantic", [JSX_APP, "src/App.jsx"])

path = os.path.join(D, "fixtures.json")
existing = json.load(open(path, encoding="utf-8-sig"))
ids = {f["id"] for f in existing}
assert not ids & {f["id"] for f in B}
merged = existing + B
with open(path, "w", encoding="utf-8") as fh:
    json.dump(merged, fh, ensure_ascii=False, indent=1)
print(f"added {len(B)} repository-IR fixtures -> {len(merged)} total")
