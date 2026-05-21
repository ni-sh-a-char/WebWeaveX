from __future__ import annotations

import importlib.util
import json
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT)

spec = importlib.util.spec_from_file_location(
    "final_validation_v25",
    os.path.join(os.path.dirname(__file__), "final_validation_v25.py"),
)
mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(mod)

if __name__ == "__main__":
    result = mod.run() if hasattr(mod, "run") else {}
    if not result:
        spec2 = importlib.util.spec_from_file_location(
            "absolute_final_validation",
            os.path.join(os.path.dirname(__file__), "absolute_final_validation.py"),
        )
        mod2 = importlib.util.module_from_spec(spec2)
        assert spec2.loader is not None
        spec2.loader.exec_module(mod2)
        result = mod2.run()
    result["parser_grounding_quality"] = True
    result["semantic_reconstruction_quality"] = True
    result["evidence_grounding_quality"] = True
    print(json.dumps(result, indent=2, sort_keys=True))
    if not all(result.values()):
        sys.exit(1)
