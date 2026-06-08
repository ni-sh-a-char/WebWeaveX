/**
 * Converted from Python: core/vision/form_extraction_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let INPUT_KEYWORDS: any = new Set(["email", "password", "username", "search"]);
export function extractForms(blocks: any): any {
  var forms: any[] = [];
  var block: any;
  for (block of py.iter(py.get(blocks, "blocks", []))) {
    var text: any = String(py.get(block, "text", "")).toLowerCase();
    if (py.contains(INPUT_KEYWORDS, text)) {
      py.listAppend(forms, {"field": text, "bbox": py.get(block, "bbox")});
    }
  }
  return {"forms": forms, "bounded": true};
}
