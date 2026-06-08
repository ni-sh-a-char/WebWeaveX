import { executeWorkflowPlan } from "../../src/workflows/workflowOrchestrator.js";
import {
  fingerprint,
  runFamily,
  printFamilyReport,
  exitOnReports,
  type CanonicalVector,
} from "./common.js";

function run(vector: CanonicalVector) {
  const plan = vector.input.plan as Record<string, unknown>;
  const output = executeWorkflowPlan(plan, Number(vector.input.tick ?? 0));
  return {
    output,
    hashes: {
      runtime_hash: fingerprint(output),
      deterministic_fingerprint: fingerprint({ input: vector.input, output }),
    },
  };
}

const report = runFamily("workflow_vectors", run);
printFamilyReport(report, "Workflow equivalence");
exitOnReports([report]);
