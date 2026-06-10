"""Execute Python (canonical) semantic-IR closure functions; emit output + hash.
Usage: PYTHONPATH=<py2.0.1> python run_python.py fixtures.json > python_results.json
"""
import importlib
import json
import sys

from core.crypto.kaalka_hash_engine import compute_kaalka_hash as H

# fn name -> module path (canonical source location)
REGISTRY = {
    "extract_rhetorical_structure": "core.documents.rhetorical_structure_engine",
    "assign_semantic_roles": "core.documents.semantic_role_engine",
    "extract_headings": "core.documents.heading_engine",
    "reconstruct_argument_dependencies": "core.documents.argument_dependency_engine",
    "resolve_coreferences": "core.documents.coreference_resolution_engine",
}


def main():
    fixtures = json.load(open(sys.argv[1], encoding="utf-8"))
    out = []
    for fx in fixtures:
        fn = fx["fn"]
        try:
            mod = importlib.import_module(REGISTRY[fn])
            result = getattr(mod, fn)(*fx["args"])
            out.append({"id": fx["id"], "fn": fn, "output": result, "hash": H(result)})
        except Exception as e:  # noqa: BLE001
            out.append({"id": fx["id"], "fn": fn,
                        "error": f"{type(e).__name__}: {e}"})
    print(json.dumps(out, ensure_ascii=False))


if __name__ == "__main__":
    main()
