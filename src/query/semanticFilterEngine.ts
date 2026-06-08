/**
 * Converted from Python: core/query/semantic_filter_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function filterSemanticRecords(records: any, predicate: any): any {
  return py.sorted(py.iter(records).filter((r: any) => py.truthy(predicate(r))).map((r: any) => r), {key: ((r: any) => py.toStr(py.get(r, "id", ""))) as (item: any) => any});
}
