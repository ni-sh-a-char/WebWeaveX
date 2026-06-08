import { runSemanticVm } from "../../src/vm/semanticVmEngine.js";
import {
  fingerprint,
  runFamily,
  printFamilyReport,
  exitOnReports,
  type CanonicalVector,
} from "./common.js";

function run(vector: CanonicalVector) {
  const instructions = (vector.input.instructions as Parameters<typeof runSemanticVm>[0]) ?? [];
  const output = runSemanticVm(instructions) as Record<string, unknown>;
  return {
    output,
    hashes: {
      vm_hash: fingerprint(output),
      runtime_hash: fingerprint(output),
      deterministic_fingerprint: fingerprint({ input: vector.input, output }),
    },
  };
}

const report = runFamily("vm_vectors", run);
printFamilyReport(report, "VM equivalence");
exitOnReports([report]);
