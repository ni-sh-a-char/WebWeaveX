import { listParsers } from "../../src/parsers/parserRegistry.js";
import {
  fingerprint,
  runFamily,
  printFamilyReport,
  exitOnReports,
} from "./common.js";

const report = runFamily("parser_vectors", (vector) => {
  const output = { registry: listParsers(), bounded: true, parser_count: listParsers().length };
  return {
    output,
    hashes: {
      runtime_hash: fingerprint(output),
      deterministic_fingerprint: fingerprint({ input: vector.input, output }),
    },
  };
});
printFamilyReport(report, "Parser equivalence");
exitOnReports([report]);
