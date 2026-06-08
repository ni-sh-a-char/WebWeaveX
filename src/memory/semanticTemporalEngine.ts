/**
 * Converted from Python: core/memory/semantic_temporal_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_SNAPSHOTS: any = 100;
export function orderTemporalSnapshots(snapshots: any): any {
  return py.slice(py.sorted(snapshots, {key: ((s: any) => [py.toInt(py.get(s, "version", 0)), py.toStr(py.get(s, "fingerprint", ""))]) as (item: any) => any}), null, MAX_SNAPSHOTS);
}
