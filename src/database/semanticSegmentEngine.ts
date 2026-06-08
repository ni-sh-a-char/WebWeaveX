/**
 * Converted from Python: core/database/semantic_segment_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_SEGMENT_SIZE: any = 10000;
export function writeSemanticSegment(path: any, records: any): any {
  var bounded: any = py.slice(records, null, MAX_SEGMENT_SIZE);
  var target: any = py.path(path);
  target.write_text(py.jsonDumps(bounded, {sortKeys: true, indent: 2, defaultStr: true}), "utf-8");
  return {"records": py.len(bounded), "path": py.toStr(target)};
}
