import { runAutonomousWorkflow } from "../../src/workflows/workflowOrchestrator.js";

const wf = runAutonomousWorkflow("extract_dashboard") as Record<string, unknown>;
const plan = wf.plan as Record<string, unknown>;
const execution = wf.execution as Record<string, unknown>;
const graph = wf.workflow_graph as Record<string, unknown>;

const results = {
  plan: plan?.objective === "extract_dashboard",
  execution:
    Array.isArray(execution?.executed) &&
    (execution.executed as Record<string, unknown>[]).every((s) => s.completed === true) &&
    execution.completed_count === (execution.executed as unknown[]).length,
  graph: Array.isArray(graph?.nodes) && (graph.nodes as unknown[]).length > 0,
};

console.log("PASS", results);
if (!Object.values(results).every(Boolean)) process.exit(1);
