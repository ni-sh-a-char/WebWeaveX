import { validateInference } from "../../src/evidence/inferenceValidation.js";

const ok = validateInference({ x: 1 }, ["e1"]);
const fail = validateInference({ x: 1 }, []);

const results = {
  valid_with_evidence: ok.valid === true,
  invalid_without: fail.valid === false,
};

console.log("PASS", results);
if (!Object.values(results).every(Boolean)) process.exit(1);
