import { detectContradictions } from "./contradictionEngine.js";
import { runOntologyRuntime } from "./ontologyRuntime.js";
import * as py from "../runtime/pyCompat.js";

export function runSemanticReasoning(
  entities: Array<Record<string, unknown>>,
  claims: Array<Record<string, unknown> | string>,
): Record<string, unknown> {
  const ontology = runOntologyRuntime(entities);
  const contradictions = detectContradictions(
    (claims ?? []).map((c) => py.toStr(c)),
  );
  return {
    ontology,
    contradictions,
    bounded: true,
    reasoning_depth: entities.length + (claims ?? []).length,
  };
}
