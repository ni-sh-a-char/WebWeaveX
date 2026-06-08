/**
 * Converted from Python: core/memory/semantic_evolution_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { trackContinuity } from "./semanticContinuityEngine.js";
import { detectSemanticChanges } from "./semanticChangeEngine.js";

export function evolveSemanticState(prior: any, current: any): any {
  var continuity: any = trackContinuity(prior, current);
  var changes: any = detectSemanticChanges(prior, current);
  var version: any = (py.truthy(prior) ? py.add(py.toInt(py.get(prior, "version", 0)), 1) : 1);
  return {"version": version, "continuity": continuity, "changes": changes, "evolved": py.at(changes, "has_changes"), "deterministic_inputs": py.get(continuity, "deterministic_inputs", [])};
}
export { detectSemanticChanges, trackContinuity };
