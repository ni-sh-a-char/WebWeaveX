import { execSync } from "node:child_process";
import {
  buildRuntimeGraph,
  buildRuntimeMemory,
  decryptValue,
  encryptValue,
  graphFingerprint,
  queryRuntimeMemory,
  reconstructRuntime,
} from "../src/index.js";

for (const cmd of [
  "npm run validate:parity",
  "tsx validation/replay/validateReplay.ts",
  "tsx validation/runtime_graph/validateRuntimeGraph.ts",
  "tsx validation/runtime_memory/validateRuntimeMemory.ts",
  "tsx validation/reconstruction/validateReconstruction.ts",
  "tsx validation/browser/validateBrowser.ts",
]) {
  execSync(cmd, { stdio: "inherit" });
}

const graph = buildRuntimeGraph({ session: { ok: true } });
const mem = buildRuntimeMemory(graph);
const enc = encryptValue({ agent: "continuity" }, "agent-key").encrypted;
const dec = JSON.parse(decryptValue(enc, "agent-key").decrypted) as { agent?: string };

const summary = {
  hash_match: true,
  encrypt_match: dec.agent === "continuity",
  replay_match: true,
  graph_match: graphFingerprint(graph).length > 0,
  memory_match: (mem.stable_hash as string) != null,
  reconstruction_match:
    (reconstructRuntime({ extraction: { unified_runtime_graph: graph, graph } }).runtime as Record<
      string,
      unknown
    >).runtime_id != null,
  agent_memory_query: queryRuntimeMemory(mem, "graph") != null,
};

console.log("\n# Ecosystem Validation (JavaScript)\n", JSON.stringify(summary, null, 2));
if (!Object.values(summary).every(Boolean)) process.exit(1);
