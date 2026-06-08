/**
 * Converted from Python: core/vision/chart_detection_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let CHART_TERMS: any = new Set(["revenue", "sales", "growth", "profit"]);
export function detectCharts(blocks: any): any {
  var detected: any = false;
  var block: any;
  for (block of py.iter(py.get(blocks, "blocks", []))) {
    var text: any = String(py.get(block, "text", "")).toLowerCase();
    if (py.any(py.iter(CHART_TERMS).map((term: any) => py.contains(text, term)))) {
      detected = true;
      break;
    }
  }
  return {"charts": [{"detected": detected}], "bounded": true};
}
