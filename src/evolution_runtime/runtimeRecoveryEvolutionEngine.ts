/**
 * Converted from Python: core/evolution_runtime/runtime_recovery_evolution_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function evolveRecoveryOrder(repairs: any): any {
  var ordering: any = py.sorted(repairs, {key: ((item: any) => py.toStr(py.get(item, "action", ""))) as (item: any) => any});
  return {"recovery_order": py.iter(ordering).map((item: any) => py.get(item, "action", "")), "evolved": true, "bounded": true};
}
