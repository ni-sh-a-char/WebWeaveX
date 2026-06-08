/**
 * Replay equivalence — prove a replayed runtime is equivalent to the original
 * (graph hash, global fingerprint, browser identity).
 *   npx tsx examples/replay-equivalence.ts
 */
import { buildRuntimeGraph, validateReplayEquivalence } from "webweavex";

const graph = buildRuntimeGraph([{ ir: "browser", nodes: [{ id: "n1" }], edges: [] }]);
const original = { unified_runtime_graph: graph, browser_ir: { runtime_identity: "id-1" } };
const replayed = structuredClone(original);

const result = validateReplayEquivalence(original, replayed);
console.log("equivalent:", result.equivalent);
for (const c of result.checks) console.log(`  ${c.name}: ${c.ok}`);
