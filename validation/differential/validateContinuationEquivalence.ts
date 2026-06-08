import { computeKaalkaHashPayload } from "../../src/crypto/kaalkaRuntime.js";
import {
  fingerprint,
  runFamily,
  printFamilyReport,
  exitOnReports,
  type CanonicalVector,
} from "./common.js";

function run(vector: CanonicalVector) {
  const session = vector.input.session as Record<string, unknown>;
  const output = {
    session_hash: computeKaalkaHashPayload(session),
    continuation: false,
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

const report = runFamily("continuation_vectors", run);
printFamilyReport(report, "Continuation equivalence");
exitOnReports([report]);
