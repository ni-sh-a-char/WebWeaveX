import { buildSemanticOntology } from "../../src/semantic/ontologyRuntime.js";
import {
  fingerprint,
  runFamily,
  printFamilyReport,
  exitOnReports,
  type CanonicalVector,
} from "./common.js";

function run(vector: CanonicalVector) {
  if (vector.id === "semantic-ontology") {
    const entities = (vector.input.entities as Array<Record<string, unknown>>) ?? [];
    const domain = String(vector.input.domain ?? "operations");
    const output = buildSemanticOntology(entities, domain);
    return {
      output,
      hashes: {
        semantic_hash: fingerprint(output),
        runtime_hash: fingerprint(output),
        deterministic_fingerprint: fingerprint({ input: vector.input, output }),
      },
    };
  }
  const output = { bounded: true };
  return { output, hashes: { runtime_hash: fingerprint(output) } };
}

const report = runFamily("semantic_vectors", run);
printFamilyReport(report, "Semantic equivalence");
exitOnReports([report]);
