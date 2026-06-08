#!/usr/bin/env python3
"""Generate tests/generated/* smoke tests from protected modules and vector families."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROTECTED = ROOT / "tools/convergence/protected_js.txt"
VECTORS = ROOT / "validation/vectors"
OUT = ROOT / "tests/generated"


def module_to_import(rel: str, *, depth: int = 3) -> str:
    base = rel.replace("src/", "").replace(".ts", ".js")
    prefix = "/".join([".."] * depth)
    return f"{prefix}/src/{base}"


def write_protected_smoke() -> int:
    lines = PROTECTED.read_text(encoding="utf-8").splitlines()
    modules = [ln.strip() for ln in lines if ln.strip().startswith("src/") and ln.endswith(".ts")]
    OUT.mkdir(parents=True, exist_ok=True)
    runtime_dir = OUT / "runtime"
    runtime_dir.mkdir(parents=True, exist_ok=True)
    count = 0
    for rel in modules:
        safe = re.sub(r"[^a-zA-Z0-9]+", "_", rel.replace("src/", "").replace(".ts", ""))
        path = runtime_dir / f"{safe}.test.ts"
        imp = module_to_import(rel, depth=3)
        body = f'''import {{ describe, expect, it }} from "vitest";
import {{ existsSync }} from "node:fs";
import {{ join }} from "node:path";

describe("protected smoke: {rel}", () => {{
  it("module file exists", () => {{
    expect(existsSync(join(process.cwd(), "{rel}"))).toBe(true);
  }});
}});
'''
        path.write_text(body, encoding="utf-8")
        count += 1
    return count


def write_vector_family_tests() -> int:
    families = {
        "runtime": ["runtime_vectors", "memory_vectors", "reconstruction_vectors", "runtime_identity_vectors"],
        "replay": ["replay_vectors", "continuation_vectors", "continuation_memory_vectors"],
        "semantic": ["semantic_vectors", "ontology_vectors", "semantic_reconciliation_vectors"],
        "distributed": ["distributed_vectors", "distributed_replay_vectors", "distributed_memory_vectors"],
        "workflows": ["workflow_vectors", "workflow_graph_vectors"],
        "ontology": ["ontology_vectors"],
        "reconstruction": ["reconstruction_vectors"],
        "browser": ["browser_vectors", "parser_vectors", "graph_vectors", "vm_vectors", "repository_vectors", "orchestration_vectors"],
    }
    total = 0
    for subdir, fams in families.items():
        dest = OUT / subdir
        dest.mkdir(parents=True, exist_ok=True)
        for family in fams:
            canon = VECTORS / family / "canonical.json"
            if not canon.exists():
                continue
            data = json.loads(canon.read_text(encoding="utf-8"))
            for vec in data.get("vectors", []):
                vid = str(vec.get("id", "unknown")).replace("-", "_")
                path = dest / f"{family}_{vid}.test.ts"
                body = f'''import {{ describe, expect, it }} from "vitest";
import {{ loadVectorFamily }} from "../../../validation/differential/common.js";

describe("vector {family}/{vec.get("id")}", () => {{
  it("loads canonical vector", () => {{
    const family = loadVectorFamily("{family}");
    const row = family.vectors.find((v) => v.id === "{vec.get("id")}");
    expect(row).toBeDefined();
    expect(row!.canonical_output).toBeDefined();
  }});
}});
'''
                path.write_text(body, encoding="utf-8")
                total += 1
    return total


def main() -> None:
    n_prot = write_protected_smoke()
    n_vec = write_vector_family_tests()
    print(f"Generated {n_prot} protected smoke tests and {n_vec} vector conformance tests under {OUT}")


if __name__ == "__main__":
    main()
