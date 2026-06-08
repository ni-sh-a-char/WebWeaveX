import { buildParserCognitionEvidence, orchestrateParserFleet } from "../../src/parsers/parserOrchestration.js";

const ev = buildParserCognitionEvidence({
  parser_evidence: { typescript: true },
  symbols: { classes: ["Foo"], functions: ["bar"] },
  dependencies: { dependencies: ["lodash"] },
  semantic_graph: { edges: [{ from: "a", to: "b" }] },
});
const fleet = orchestrateParserFleet([{ parser_evidence: { js: true } }]);

const results = {
  parser_evidence: (ev.parser_evidence as string[]).length > 0,
  fleet: (fleet.count as number) === 1,
};

console.log("PASS", results);
if (!Object.values(results).every(Boolean)) process.exit(1);
