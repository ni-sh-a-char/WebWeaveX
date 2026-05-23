import {
  buildRuntimeGraph,
  buildRuntimeMemory,
  mergeRuntimeMemories,
  queryRuntimeMemory,
  stableMemoryHash,
} from "../../src/index.js";

const graph = buildRuntimeGraph({ session: { ok: true } });
const mem = buildRuntimeMemory(graph, [{ step: 1, kind: "workflow" }]);
const results = {
  memory_match:
    (mem.stable_hash as string) === stableMemoryHash(graph, [{ step: 1, kind: "workflow" }]),
  query_match: queryRuntimeMemory(mem, "graph") != null,
  merge_match: mergeRuntimeMemories(mem, mem).bounded === true,
  deterministic:
    (mem.stable_hash as string) ===
    (buildRuntimeMemory(graph, [{ step: 1, kind: "workflow" }]).stable_hash as string),
};
const allOk = Object.values(results).every(Boolean);
console.log(allOk ? "PASS" : "FAIL", results);
if (!allOk) process.exit(1);
