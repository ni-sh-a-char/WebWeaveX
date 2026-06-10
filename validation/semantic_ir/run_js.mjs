// Execute JS semantic-IR engine functions; emit output + hash.
//   cp run_js.mjs <js-ref>/ && (cd <js-ref> && npx tsx run_js.mjs <abs fixtures.json>)
//
// Hashing: the canonical digest is Python's compute_kaalka_hash =
// sha256(stable_serialize(value)). The JS branch's computeKaalkaHash diverges
// from that definition for float-typed outputs of py2ts-generated engines
// (PyFloat boxes are recursed as plain objects, and fast-json-stable-stringify
// renders integral floats as "0" where Python emits "0.0"). pyStableHash below
// applies the canonical Python payload definition to the JS engine's typed
// output using the engine's own Python-faithful serializer (pyCompat.jsonDumps,
// PyFloat -> "0.0"), so hash equality proves float-typed value equality.
import { readFileSync } from "node:fs";
import { createHash } from "node:crypto";
import * as py from "./src/runtime/pyCompat.ts";
// A.1 — document parser leaves
import { extractRhetoricalStructure } from "./src/documents/rhetoricalStructureEngine.ts";
import { assignSemanticRoles } from "./src/documents/semanticRoleEngine.ts";
import { extractHeadings } from "./src/documents/headingEngine.ts";
import { reconstructArgumentDependencies } from "./src/documents/argumentDependencyEngine.ts";
import { resolveCoreferences } from "./src/documents/coreferenceResolutionEngine.ts";
// A.2 — semantic pressure leaves
import { computeAmbiguityPressure } from "./src/semantic/ambiguityPressureEngine.ts";
import { computeContradictionPressure } from "./src/semantic/contradictionPressureEngine.ts";
import { computeEvidenceBoundaryPressure } from "./src/semantic/evidenceBoundaryPressureEngine.ts";
import { computeEvidenceDecayPressure } from "./src/semantic/evidenceDecayPressureEngine.ts";
import { computeRecursiveBoundaryPressure } from "./src/semantic/recursiveBoundaryPressureEngine.ts";
import { computeRecursiveConvergencePressure } from "./src/semantic/recursiveConvergencePressureEngine.ts";
import { computeRecursiveDependencyPressure } from "./src/semantic/recursiveDependencyPressureEngine.ts";
import { computeSemanticBoundaryPressure } from "./src/semantic/semanticBoundaryPressureEngine.ts";
import { computeTruthBoundaryPressure } from "./src/semantic/truthBoundaryPressureEngine.ts";
import { computeUncertaintyPressure } from "./src/semantic/uncertaintyPressureEngine.ts";
// A.2 — ir/_base leaves
import { emptyConfidence, emptyLineage, mergeEvidence } from "./src/ir/_base.ts";
// A.2 — graph leaves
import { modelGraphEntropy } from "./src/graph/graphEntropyEngine.ts";
import { detectCycles } from "./src/graph/semanticCycleAnalysisEngine.ts";
import { proveTopology } from "./src/graph/topologyProofEngine.ts";
// A.2 — repository leaves
import { reasonApiSurface } from "./src/repository/apiSurfaceReasoningEngine.ts";
import { reconstructExecutionFlow } from "./src/repository/executionFlowEngine.ts";
import { detectInfraSignals } from "./src/repository/infraSemanticEngine.ts";
import { resolveRuntimeDependencies } from "./src/repository/runtimeDependencyEngine.ts";
import { inferServiceInteractions } from "./src/repository/serviceInteractionEngine.ts";
// A.2 — ast leaves
import { buildControlFlowGraph } from "./src/ast/controlFlowEngine.ts";
import { reconstructExecutionPaths } from "./src/ast/executionPathEngine.ts";
import { resolveSymbols } from "./src/ast/symbolResolutionEngine.ts";

const VOLATILE = new Set([
  "timestamp", "created_at", "updated_at", "nonce", "request_id",
  "csrf", "generated_at", "runtime_id", "random", "uuid",
]);

const isPlainObj = (v) =>
  v !== null && typeof v === "object" && !Array.isArray(v) && !py.isF(v);

// Python core.determinism.normalization.stable_sort_keys (PyFloat-preserving).
function stableSortKeysPy(obj) {
  const out = {};
  for (const k of Object.keys(obj).sort()) {
    if (VOLATILE.has(k)) continue;
    const v = obj[k];
    if (isPlainObj(v)) out[k] = stableSortKeysPy(v);
    else if (Array.isArray(v)) out[k] = v.map((it) => (isPlainObj(it) ? stableSortKeysPy(it) : it));
    else out[k] = v;
  }
  return out;
}

// Python core.determinism.normalization.stable_serialize + sha256.
function pyStableHash(value) {
  const opts = { sortKeys: true, ensureAscii: false, separators: [",", ":"] };
  let payload;
  if (typeof value === "string") {
    payload = value.normalize("NFKC").replace(/\r\n/g, "\n").replace(/\r/g, "\n").replace(/\s+$/, "");
  } else if (isPlainObj(value)) {
    payload = py.jsonDumps(stableSortKeysPy(value), opts);
  } else if (Array.isArray(value)) {
    const keyed = {};
    value.forEach((it, i) => { keyed[String(i)] = isPlainObj(it) ? stableSortKeysPy(it) : it; });
    payload = py.jsonDumps(keyed, opts);
  } else {
    payload = py.jsonDumps(value, { ensureAscii: false, separators: [",", ":"] });
  }
  return createHash("sha256").update(payload, "utf8").digest("hex");
}

function call(fn, args) {
  switch (fn) {
    case "extract_rhetorical_structure":
      return extractRhetoricalStructure(args[0]);
    case "assign_semantic_roles":
      return assignSemanticRoles(args[0]);
    case "extract_headings":
      return extractHeadings(args[0]);
    case "reconstruct_argument_dependencies":
      return reconstructArgumentDependencies(args[0]);
    case "resolve_coreferences":
      return resolveCoreferences(args[0]);
    case "compute_ambiguity_pressure":
      return computeAmbiguityPressure(args[0]);
    case "compute_contradiction_pressure":
      return computeContradictionPressure(args[0]);
    case "compute_evidence_boundary_pressure":
      return args.length > 1 ? computeEvidenceBoundaryPressure(args[0], args[1]) : computeEvidenceBoundaryPressure(args[0]);
    case "compute_evidence_decay_pressure":
      return args.length > 1 ? computeEvidenceDecayPressure(args[0], args[1]) : computeEvidenceDecayPressure(args[0]);
    case "compute_recursive_boundary_pressure":
      return computeRecursiveBoundaryPressure(args[0], args[1]);
    case "compute_recursive_convergence_pressure":
      return computeRecursiveConvergencePressure(args[0], args[1]);
    case "compute_recursive_dependency_pressure":
      return computeRecursiveDependencyPressure(args[0], args[1]);
    case "compute_semantic_boundary_pressure":
      return computeSemanticBoundaryPressure(args[0], args[1]);
    case "compute_truth_boundary_pressure":
      return computeTruthBoundaryPressure(args[0], args[1]);
    case "compute_uncertainty_pressure":
      return computeUncertaintyPressure(args[0], args[1]);
    case "empty_confidence":
      return emptyConfidence();
    case "empty_lineage":
      return args.length ? emptyLineage(args[0]) : emptyLineage();
    case "merge_evidence":
      return mergeEvidence(...args);
    case "model_graph_entropy":
      return modelGraphEntropy(args[0]);
    case "detect_cycles":
      return detectCycles(args[0]);
    case "prove_topology":
      return proveTopology(args[0]);
    case "reason_api_surface":
      return reasonApiSurface(args[0]);
    case "reconstruct_execution_flow":
      return reconstructExecutionFlow(args[0]);
    case "detect_infra_signals":
      return detectInfraSignals(args[0]);
    case "resolve_runtime_dependencies":
      return args.length > 1 ? resolveRuntimeDependencies(args[0], args[1]) : resolveRuntimeDependencies(args[0]);
    case "infer_service_interactions":
      return inferServiceInteractions(args[0], args[1]);
    case "build_control_flow_graph":
      return buildControlFlowGraph(args[0]);
    case "reconstruct_execution_paths":
      return reconstructExecutionPaths(args[0]);
    case "resolve_symbols":
      return resolveSymbols(args[0]);
    default:
      throw new Error("unknown fn " + fn);
  }
}

const fixtures = JSON.parse(readFileSync(process.argv[2], "utf-8"));
const out = [];
for (const fx of fixtures) {
  try {
    const result = call(fx.fn, fx.args);
    out.push({ id: fx.id, fn: fx.fn, output: result, hash: pyStableHash(result) });
  } catch (e) {
    out.push({ id: fx.id, fn: fx.fn, error: String(e && e.message ? e.message : e) });
  }
}
process.stdout.write(JSON.stringify(out));
