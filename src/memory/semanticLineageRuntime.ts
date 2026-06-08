/**
 * Converted from Python: core/memory/semantic_lineage_runtime.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_LINEAGE: any = 200;
export function recordSemanticLineage(entries: any): any {
  var ordered: any = py.slice(py.sorted(entries, {key: ((e: any) => [py.toInt(py.get(e, "version", 0)), py.toStr(py.get(e, "id", ""))]) as (item: any) => any}), null, MAX_LINEAGE);
  return {"lineage": ordered, "count": py.len(ordered), "deterministic": true, "bounded": true};
}
