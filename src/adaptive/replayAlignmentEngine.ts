/**
 * Converted from Python: core/adaptive/replay_alignment_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function alignReplayState(expected: any, actual: any): any {
  var aligned: any[] = [];
  var index: any;
  var item: any;
  for ([index, item] of py.enumerate(expected)) {
    var actual_item: any = ((index < py.len(actual)) ? py.at(actual, index) : {});
    py.listAppend(aligned, {"step": index, "expected": item, "actual": actual_item, "matched": py.eq(item, actual_item)});
  }
  return {"aligned": aligned, "fully_aligned": py.all(py.iter(aligned).map((step: any) => py.at(step, "matched"))), "bounded": true};
}
