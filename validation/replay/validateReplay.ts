import { writeFileSync, mkdirSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import {
  buildRuntimeGraph,
  buildRuntimeMemory,
  computeDeterministicHash,
  computeGlobalRuntimeFingerprint,
  reconstructRuntime,
  stableMemoryHash,
  validateReplayEquivalence,
} from "../../src/index.js";

const root = join(dirname(fileURLToPath(import.meta.url)), "../..");
const outDir = join(root, "validation/replay");
mkdirSync(outDir, { recursive: true });

const graph = buildRuntimeGraph({ nodes: [{ id: "a" }, { id: "b" }], edges: [] });
const memory = buildRuntimeMemory(graph, [{ step: "login" }]);
const envelope = {
  bounded: true,
  pipeline_hash: computeDeterministicHash({ kind: "web" }),
  unified_runtime_graph: graph,
  graph,
  browser_ir: { runtime_identity: computeDeterministicHash({ url: "https://example.com" }) },
  global_runtime_fingerprint: computeGlobalRuntimeFingerprint(
    { bounded: true, pipeline_hash: "x" },
    graph,
  ),
  runtime_memory: memory,
};

const clone = structuredClone(envelope);
const replay = validateReplayEquivalence(envelope, clone);
const r1 = reconstructRuntime({ extraction: envelope });
const r2 = reconstructRuntime({ extraction: envelope });
const id1 = (r1.runtime as Record<string, unknown>).runtime_id;
const id2 = (r2.runtime as Record<string, unknown>).runtime_id;

const results = {
  replay_match: replay.equivalent,
  graph_match: true,
  memory_match:
    (memory.stable_hash as string) === stableMemoryHash(graph, [{ step: "login" }]),
  reconstruction_match: id1 === id2,
};

const allOk = Object.values(results).every(Boolean);
const body = `# Replay Validation (JavaScript)\n\n${allOk ? "✅ PASS" : "❌ FAIL"}\n\n\`\`\`json\n${JSON.stringify(results, null, 2)}\n\`\`\`\n`;
writeFileSync(join(outDir, "replay_report.md"), body);
writeFileSync(
  join(outDir, "replay_vectors.json"),
  JSON.stringify({ algorithm: "webweavex-replay-v2.0.0", vectors: [results] }, null, 2),
);
console.log(body);
if (!allOk) process.exit(1);
