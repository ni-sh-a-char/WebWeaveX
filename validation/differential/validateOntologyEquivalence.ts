import { buildSemanticOntology } from "../../src/semantic/ontologyRuntime.js";
import { fingerprint, runFamily, printFamilyReport, exitOnReports, type CanonicalVector } from "./common.js";

function run(vector: CanonicalVector) {
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

const report = runFamily("ontology_vectors", run);
printFamilyReport(report, "Ontology equivalence");
exitOnReports([report]);
