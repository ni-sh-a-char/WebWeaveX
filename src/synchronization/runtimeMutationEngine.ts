/**
 * Converted from Python: core/synchronization/runtime_mutation_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function trackRuntimeMutations(changes: any, tick: any = 0): any {
  return {"mutations": py.sorted(changes, {key: ((item: any) => py.toStr(py.get(item, "field", ""))) as (item: any) => any}), "count": py.len(changes), "tick": tick, "bounded": true};
}
