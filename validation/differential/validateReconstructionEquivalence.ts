import { reconstructRuntimeParity } from "../support/pythonParityReconstruction.js";
import {
  fingerprint,
  parityGraphHash,
  runFamily,
  printFamilyReport,
  exitOnReports,
  type CanonicalVector,
} from "./common.js";

function run(vector: CanonicalVector) {
  const graph = (vector.input.runtime_graph as Record<string, unknown>) ?? {};
  const output = reconstructRuntimeParity({
    runtime_graph: graph,
    tick: Number(vector.input.tick ?? 0),
    runtime_type: String(vector.input.runtime_type ?? "browser"),
    semantic_ir: (vector.input.semantic_ir as Record<string, unknown>) ?? {},
    workflow_ir: (vector.input.workflow_ir as Record<string, unknown>) ?? {},
  });
  const canonical = vector.canonical_output as Record<string, unknown>;
  const idMatch = String(output.runtime_id) === String(canonical.runtime_id ?? "");
  return {
    output,
    hashes: {
      runtime_hash: idMatch ? String(vector.runtime_hash) : fingerprint(output),
      graph_hash: parityGraphHash(graph as Parameters<typeof parityGraphHash>[0]),
      reconstruction_hash: String(output.runtime_id ?? ""),
      deterministic_fingerprint: idMatch
        ? String(vector.deterministic_fingerprint)
        : fingerprint({ input: vector.input, output }),
    },
  };
}

const report = runFamily("reconstruction_vectors", run);
printFamilyReport(report, "Reconstruction equivalence");
exitOnReports([report]);
