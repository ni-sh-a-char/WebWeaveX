/**
 * Converted from Python: core/vision/ui_component_detection_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let BUTTON_KEYWORDS: any = new Set(["submit", "login", "sign in", "continue"]);
export function detectUiComponents(blocks: any): any {
  var components: any[] = [];
  var block: any;
  for (block of py.iter(py.get(blocks, "blocks", []))) {
    var text: any = String(py.get(block, "text", "")).toLowerCase();
    if (py.contains(BUTTON_KEYWORDS, text)) {
      py.listAppend(components, {"type": "button", "text": text, "bbox": py.get(block, "bbox")});
    }
  }
  return {"components": components, "bounded": true};
}
