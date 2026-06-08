/**
 * Converted from Python: core/semantic/document_semantics_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let DOC_KIND_RULES: any = [["contract", py.regex("agreement|terms|party|signature", "i")], ["technical_doc", py.regex("architecture|module|implementation", "i")], ["api_reference", py.regex("endpoint|request|response|openapi", "i")], ["invoice", py.regex("invoice|amount due|tax", "i")], ["report", py.regex("summary|findings|quarter|annual", "i")], ["resume", py.regex("experience|education|skills", "i")], ["legal", py.regex("whereas|jurisdiction|liability", "i")], ["specification", py.regex("requirements|shall|must|specification", "i")]];
export function extractDocumentSemantics(text: any = ""): any {
  var kinds: any = py.iter(DOC_KIND_RULES).filter(([kind, pattern]: any) => py.truthy(pattern.search(text))).map(([kind, pattern]: any) => kind);
  if (!py.truthy(kinds)) {
    kinds = ["document"];
  }
  return {"kinds": py.sorted(kinds), "primary_kind": py.at(py.sorted(kinds), 0), "length": py.len(text), "bounded": true};
}
