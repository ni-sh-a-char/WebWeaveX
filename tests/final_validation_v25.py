from __future__ import annotations

import importlib.util
import json
import os
import sys
from pathlib import Path

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT)

spec = importlib.util.spec_from_file_location(
    "absolute_final_validation",
    os.path.join(os.path.dirname(__file__), "absolute_final_validation.py"),
)
mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(mod)

if __name__ == "__main__":
    result = mod.run()
    enrich = Path(ROOT) / "core" / "extract" / "enrichment_engine.py"
    text = enrich.read_text(encoding="utf-8")
    result["enrichment_import_fanout"] = "facades._imports" not in text
    root = Path(ROOT)
    result["namespace_trees_removed"] = not (root / "core" / "graph" / "v6").exists()
    result["facade_split_ok"] = (root / "core" / "extract" / "facades" / "parser_facade.py").exists()
    result["no_mega_imports"] = not (root / "core" / "extract" / "facades" / "_imports.py").exists()
    print(json.dumps(result, indent=2, sort_keys=True))
    if not all(result.values()):
        sys.exit(1)
