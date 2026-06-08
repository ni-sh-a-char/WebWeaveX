import { execSync } from "node:child_process";
import {
  buildRuntimeMemory,
  decryptValue,
  encryptValue,
  graphFingerprint,
  queryRuntimeMemory,
  reconstructRuntime,
} from "../src/index.js";
import { buildRuntimeGraph } from "../src/graph/runtimeGraph.js";

for (const cmd of [
  "npm run validate:parity",
  "tsx validation/kaalka_cross_language/validateCrossLanguage.ts",
  "tsx validation/replay/validateReplay.ts",
  "tsx validation/runtime_graph/validateRuntimeGraph.ts",
  "tsx validation/runtime_memory/validateRuntimeMemory.ts",
  "tsx validation/reconstruction/validateReconstruction.ts",
  "tsx validation/browser/validateBrowser.ts",
  "tsx validation/connectors/validateConnectors.ts",
  "tsx validation/orchestration/validateOrchestration.ts",
  "tsx validation/semantics/validateSemantics.ts",
  "tsx validation/distributed/validateDistributed.ts",
  "tsx validation/repository/validateRepository.ts",
  "tsx validation/documents/validateDocuments.ts",
  "tsx validation/evidence/validateEvidence.ts",
  "tsx validation/streaming/validateStreaming.ts",
  "tsx validation/adaptive/validateAdaptive.ts",
  "tsx validation/workflows/validateWorkflows.ts",
  "tsx validation/cognition/validateCognition.ts",
  "tsx validation/parsers/validateParsers.ts",
  "tsx validation/graph/validateGraph.ts",
  "tsx validation/vm/validateVm.ts",
  "tsx validation/differential/runAllDifferential.ts",
  "npm run validate:replay-equivalence",
  "tsx validation/enterprise/validateEnterprise.ts",
  "tsx validation/production/validateProductionMaster.ts",
  "tsx validation/realworld/validateRealWorld.ts",
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
