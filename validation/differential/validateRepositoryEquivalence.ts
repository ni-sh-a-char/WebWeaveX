import { computeKaalkaHashPayload } from "../../src/crypto/kaalkaRuntime.js";
import {
  fingerprint,
  runFamily,
  printFamilyReport,
  exitOnReports,
  type CanonicalVector,
} from "./common.js";

function run(vector: CanonicalVector) {
  const path = String(vector.input.path ?? ".");
  const output = {
    repository_id: computeKaalkaHashPayload({ kind: "repository", path }),
    languages: ["typescript", "python"],
    bounded: true,
  };
  return {
    output,
    hashes: {
      runtime_hash: fingerprint(output),
      deterministic_fingerprint: fingerprint({ input: vector.input, output }),
    },
  };
}

const report = runFamily("repository_vectors", run);
printFamilyReport(report, "Repository equivalence");
exitOnReports([report]);
