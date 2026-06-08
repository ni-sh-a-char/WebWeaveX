/**
 * Converted from Python: core/reasoning/discourse_reasoning_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import { compileDocumentIr } from "../ir/documentIr.js";
import { analyzeLongRangeDiscourse } from "../documents/longRangeDiscourseEngine.js";

export function reasonDiscourseSemantic(text: any): any {
  var ir: any = compileDocumentIr(text);
  var long_range: any = analyzeLongRangeDiscourse(text);
  return {"ir": ir, "long_range": long_range, "explainable": true};
}
export { analyzeLongRangeDiscourse, compileDocumentIr };
