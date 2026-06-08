import { runDistributedExtraction } from "../../src/distributed/distributedExtractionOrchestrator.js";
import {
  fingerprint,
  runFamily,
  printFamilyReport,
  exitOnReports,
  type CanonicalVector,
} from "./common.js";

function run(vector: CanonicalVector) {
  const tasks = (vector.input.tasks as Record<string, unknown>[]) ?? [];
  const output = runDistributedExtraction(tasks, undefined, {}, 0, []) as Record<string, unknown>;
  return {
    output,
    hashes: {
      runtime_hash: fingerprint(output),
      deterministic_fingerprint: fingerprint({ input: vector.input, output }),
    },
  };
}

const report = runFamily("distributed_vectors", run);
printFamilyReport(report, "Distributed equivalence");
exitOnReports([report]);
