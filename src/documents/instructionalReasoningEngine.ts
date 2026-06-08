/**
 * Converted from Python: core/documents/instructional_reasoning_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import { analyzeInstructionalSemantics } from "./instructionalSemanticsEngine.js";

export function reasonInstructional(text: any): any {
  return analyzeInstructionalSemantics(text);
}
export { analyzeInstructionalSemantics };
