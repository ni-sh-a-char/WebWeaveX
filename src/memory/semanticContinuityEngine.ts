/**
 * Converted from Python: core/memory/semantic_continuity_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function trackContinuity(prior: any, current: any): any {
  var pk: any = py.toSet(py.keys(prior).map((k: any) => py.toStr(k)));
  var ck: any = py.toSet(py.keys(current).map((k: any) => py.toStr(k)));
  return {"continuous_keys": py.sorted(py.bitand(pk, ck)), "added_keys": py.sorted(py.sub(ck, pk)), "removed_keys": py.sorted(py.sub(pk, ck)), "continuous": py.or2((py.len(py.bitand(pk, ck)) > 0), () => (!py.truthy(prior))), "deterministic_inputs": [`prior=${py.toStr(py.len(pk))}`, `current=${py.toStr(py.len(ck))}`]};
}
