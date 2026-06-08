import { describe, expect, it } from "vitest";
import { existsSync } from "node:fs";
import { join } from "node:path";
import { loadVectorFamily } from "../../validation/differential/common.js";

const VECTOR_FAMILIES = [
  "graph_vectors",
  "runtime_vectors",
  "memory_vectors",
  "replay_vectors",
  "vm_vectors",
  "repository_vectors",
  "browser_vectors",
  "parser_vectors",
];

describe("generated vector conformance", () => {
  for (const family of VECTOR_FAMILIES) {
    it(`loads ${family} canonical.json`, () => {
      const path = join("validation/vectors", family, "canonical.json");
      if (!existsSync(path)) {
        console.warn(`Skip ${family}: run python tools/runtime_vectors/generate_canonical_vectors.py`);
        return;
      }
      const data = loadVectorFamily(family);
      expect(data.vectors.length).toBeGreaterThan(0);
      expect(["webweavex-spec", "origin/python"]).toContain(data.source);
    });
  }
});
