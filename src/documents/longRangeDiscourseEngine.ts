/**
 * Converted from Python: core/documents/long_range_discourse_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { buildDocumentSemanticIr } from "./documentSemanticIrEngine.js";

export function analyzeLongRangeDiscourse(text: any, max_span: any = 5000): any {
  var bounded: any = py.slice(py.or2(text, () => ("")), null, max_span);
  var ir: any = buildDocumentSemanticIr(bounded);
  return {"ir": ir, "bounded_chars": py.len(bounded), "long_range_links": py.slice(py.get(py.get(ir, "coreference", {}), "edges", []), null, 50), "evidence": py.get(ir, "evidence", [])};
}
export { buildDocumentSemanticIr };
