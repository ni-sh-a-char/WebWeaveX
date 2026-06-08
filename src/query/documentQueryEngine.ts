/**
 * Converted from Python: core/query/document_query_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { compileDocumentIr } from "../ir/documentIr.js";

export function queryDocuments(text: any): any {
  var ir: any = compileDocumentIr(text);
  return {"ir": ir, "claims": py.get(ir, "claims", []), "tutorial_steps": py.get(ir, "tutorial_steps", []), "explainable": true};
}
export { compileDocumentIr };
