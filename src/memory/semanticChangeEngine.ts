/**
 * Converted from Python: core/memory/semantic_change_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { diffSemanticIr } from "./semanticDiffEngine.js";

export function detectSemanticChanges(before: any, after: any): any {
  var diff: any = diffSemanticIr(before, after);
  return {...(diff), "has_changes": (py.at(diff, "change_count") > 0)};
}
export { diffSemanticIr };
