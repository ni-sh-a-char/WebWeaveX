/**
 * Converted from Python: core/query/semantic_resolution_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import { resolveEntities } from "../knowledge/entityResolutionEngine.js";

export function semanticResolve(candidates: any, namespace: any = "query"): any {
  return resolveEntities(candidates, namespace);
}
export { resolveEntities };
