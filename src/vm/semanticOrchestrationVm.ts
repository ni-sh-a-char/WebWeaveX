import { runSemanticOrchestration } from "../semantic/semanticOrchestration.js";

export function executeOrchestrationVm(
  states: Record<string, unknown>[],
): Record<string, unknown> {
  const orchestration = runSemanticOrchestration(states);
  return { ...orchestration, vm: "orchestration", depth: orchestration.depth, bounded: true };
}
