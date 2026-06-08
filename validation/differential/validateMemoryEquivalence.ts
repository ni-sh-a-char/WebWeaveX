import { buildRuntimeMemoryParity } from "../support/pythonParityMemory.js";
import {
  fingerprint,
  runFamily,
  printFamilyReport,
  exitOnReports,
  type CanonicalVector,
} from "./common.js";

function run(vector: CanonicalVector) {
  const history = (vector.input.history as Array<Record<string, unknown>>) ?? [];
  const mem = buildRuntimeMemoryParity({
    runtime_history: history,
    lineage: (vector.input.lineage as Array<Record<string, unknown>>) ?? [{ id: "L1" }],
  });
  return {
    output: mem,
    hashes: {
      runtime_hash: fingerprint(mem),
      memory_hash: String(mem.stable_hash ?? ""),
      deterministic_fingerprint: fingerprint({ input: vector.input, output: mem }),
    },
  };
}

const report = runFamily("memory_vectors", run);
printFamilyReport(report, "Memory equivalence");
exitOnReports([report]);
