// Cross-product driver — JavaScript side. Run from the javascript worktree:
//   npx tsx cross_js.mjs <vec_dir> <signatures.json> <out.json>
// Calls each {api, input|args} vector positionally using the Python signature
// order (generated ports preserve Python parameter names/order), with the same
// per-API adapters as cross_py.py / the Dart parity tests.
import { readFileSync, writeFileSync, readdirSync } from "node:fs";
import { join } from "node:path";
import * as W from "./src/index.ts";
import { computeKaalkaHash } from "./src/crypto/kaalkaRuntime.ts";
import { buildRuntimeMemory } from "./src/memory/runtimeMemoryEngine.ts";
import { queryRuntimeMemory } from "./src/memory/runtimeQueryEngine.ts";
import { buildBrowserIdentity } from "./src/identity/browserIdentityOrchestrator.ts";
import { computeGlobalRuntimeFingerprint } from "./src/determinism/globalRuntimeFingerprint.ts";
import { queryRuntimeGraph } from "./src/runtime_graph/runtimeGraphQueryEngine.ts";
import { validateReplayEquivalence } from "./src/replay/replayEquivalenceEngine.ts";
import { reconstructRuntime } from "./src/reconstruction/runtimeReconstructionEngine.ts";
import { getRuntimeKernel } from "./src/kernel/runtimeKernel.ts";
import { executeRuntimeObjective } from "./src/application/objectiveExecutionEngine.ts";
import { buildRuntimePermissions } from "./src/execution/runtimePermissionsEngine.ts";
// Python-aligned orchestrator ports (the public index exports JS-variant shapes).
import { runSemanticRuntime } from "./src/semantic/semanticOrchestrator.ts";
import {
  runReconstructionRuntime,
  runReconstructionForExtraction,
} from "./src/reconstruction/runtimeReconstructionOrchestrator.ts";
import {
  runSynchronizedRuntime,
  runSyncForExtraction,
} from "./src/synchronization/runtimeSyncOrchestrator.ts";
import { runExecutionRuntime } from "./src/execution/runtimeExecutionOrchestrator.ts";
import { healSelector } from "./src/adaptive/selectorHealingEngine.ts";

const [vecDir, sigPath, outPath] = process.argv.slice(2);
const signatures = JSON.parse(readFileSync(sigPath, "utf-8"));

const camel = (s) => s.replace(/_([a-z0-9])/g, (_, c) => c.toUpperCase());

// Canonical engine-function overrides (JS public index exports variants).
const FN_OVERRIDES = {
  build_runtime_memory: buildRuntimeMemory,
  query_runtime_memory: queryRuntimeMemory,
  build_browser_identity: buildBrowserIdentity,
  compute_global_runtime_fingerprint: computeGlobalRuntimeFingerprint,
  query_runtime_graph: queryRuntimeGraph,
  validate_replay_equivalence: validateReplayEquivalence,
  reconstruct_runtime: reconstructRuntime,
  execute_runtime_objective: executeRuntimeObjective,
  run_semantic_runtime: runSemanticRuntime,
  run_reconstruction_runtime: runReconstructionRuntime,
  run_reconstruction_for_extraction: runReconstructionForExtraction,
  run_synchronized_runtime: runSynchronizedRuntime,
  run_sync_for_extraction: runSyncForExtraction,
  run_execution_runtime: runExecutionRuntime,
  heal_selector: healSelector,
};

const ADAPTERS = {
  replay_interactions: (v) => W.replayInteractions(null, v.input.interaction_log),
  replay_stream_events: (v) => W.replayStreamEvents(null, v.input.stream_log),
  decrypt_session_state: (v) =>
    W.decryptSessionState(W.encryptSessionState(v.input.session, v.input.key), v.input.key),
  execute_runtime_action: (v) =>
    W.executeRuntimeAction(
      v.input.raw_action,
      "sandbox" in v.input ? W.buildRuntimeSandbox(v.input.sandbox) : null,
      null,
      "permissions" in v.input ? buildRuntimePermissions(v.input.permissions) : null,
      v.input.tick ?? 0,
    ),
  simulate_runtime_execution: (v) =>
    W.simulateRuntimeExecution(
      v.input.actions,
      "sandbox" in v.input ? W.buildRuntimeSandbox(v.input.sandbox) : null,
      v.input.tick ?? 0,
    ),
  get_runtime_kernel: (v) => ({ runtime_type: getRuntimeKernel(...(v.args ?? [])).runtime_type }),
  analyze: (v) => W.analyze(v.input.nodes, v.input.edges ?? null),
};

function call(v) {
  if (v.api in ADAPTERS) return ADAPTERS[v.api](v);
  const fn = FN_OVERRIDES[v.api] ?? W[camel(v.api)] ?? W[v.api];
  if (typeof fn !== "function") throw new Error("MISSING-IN-JS: " + v.api);
  if (v.args) return fn(...v.args.map((a) => (a === null ? undefined : a)));
  const params = signatures[v.api];
  if (!params) throw new Error("NO-SIGNATURE: " + v.api);
  const args = params.map((p) => (p in v.input ? v.input[p] : undefined));
  // trim trailing undefined so defaults apply
  while (args.length && args[args.length - 1] === undefined) args.pop();
  if (args.length === 0 && Object.keys(v.input).length > 0) {
    return fn(v.input);
  }
  return fn(...args);
}

const results = {};
let total = 0, match = 0, mismatch = 0, errors = 0, scenario = 0;
for (const fname of readdirSync(vecDir).filter((f) => f.endsWith("_api_vectors.json")).sort()) {
  if (fname.startsWith("semantic_ir_")) continue; // dedicated harness (phase 12)
  const vectors = JSON.parse(readFileSync(join(vecDir, fname), "utf-8"));
  const rows = [];
  vectors.forEach((v, i) => {
    if (!(v.api in ADAPTERS) && !(v.api in FN_OVERRIDES) && !W[camel(v.api)] && !W[v.api]) {
      rows.push({ i, api: v.api, status: "SCENARIO-SKIP" });
      scenario++;
      return;
    }
    total++;
    let h;
    try {
      h = computeKaalkaHash(call(v));
    } catch (e) {
      rows.push({ i, api: v.api, status: "ERROR", error: String(e?.message ?? e).slice(0, 200) });
      errors++;
      return;
    }
    const committed = "expected" in v ? computeKaalkaHash(v.expected) : v.det_hash;
    const ok = h === committed;
    ok ? match++ : mismatch++;
    rows.push({ i, api: v.api, status: ok ? "MATCH" : "MISMATCH", live_hash: h, committed_hash: committed });
  });
  results[fname] = rows;
}
const summary = { vector_files: Object.keys(results).length, vectors_executed: total,
  match_committed: match, mismatch_committed: mismatch, errors, scenario_skips: scenario };
writeFileSync(outPath, JSON.stringify({ summary, results }, null, 1));
console.log(JSON.stringify(summary, null, 1));
