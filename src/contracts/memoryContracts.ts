/**
 * Converted from Python: core/contracts/memory_contracts.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export class MemorySnapshotContract {
  static canonicalize(snapshot: any): any {
    var history: any = [...py.iter(py.get(snapshot, "runtime_history", []))];
    var history_sorted: any = py.sorted(history, {key: ((h: any) => [py.toInt(py.get(h, "tick", 0)), py.toStr(py.get(h, "kind", "")), py.toStr(py.get(h, "source", ""))]) as (item: any) => any});
    return {...(Object.fromEntries(py.iter(py.sorted(py.items(snapshot))).filter(([k, v]: any) => !py.eq(k, "runtime_history")).map(([k, v]: any) => ([k, v] as [any, any])))), "runtime_history": history_sorted, "bounded": true};
  }
}
