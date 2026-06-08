/**
 * Converted from Python: core/repository/runtime_diff_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import { diffSemanticIr } from "../memory/semanticDiffEngine.js";

export function diffRuntimeIr(before: any, after: any): any {
  return diffSemanticIr(before, after);
}
export { diffSemanticIr };
