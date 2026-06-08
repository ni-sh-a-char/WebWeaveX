/**
 * Converted from Python: core/layout/layout_detection_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_BLOCKS: any = 10000;
export function detectLayoutBlocks(ocr_regions: any): any {
  var blocks: any[] = [];
  var idx: any;
  var region: any;
  for ([idx, region] of py.enumerate(py.slice(ocr_regions, null, MAX_BLOCKS))) {
    py.listAppend(blocks, {"id": `block_${py.toStr(idx)}`, "bbox": py.get(region, "bbox"), "text": py.get(region, "text", ""), "type": "text_block"});
  }
  return {"blocks": blocks, "bounded": true};
}
