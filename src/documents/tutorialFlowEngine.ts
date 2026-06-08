/**
 * Converted from Python: core/documents/tutorial_flow_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import { analyzeInstructionalSemantics } from "./instructionalSemanticsEngine.js";

export function extractTutorialFlow(text: any): any {
  return analyzeInstructionalSemantics(text);
}
export { analyzeInstructionalSemantics };
