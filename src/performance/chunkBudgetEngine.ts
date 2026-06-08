/**
 * Converted from Python: core/performance/chunk_budget_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function budgetedChunks(text: any, chunk_size: any = 50000): any {
  var raw: any = py.or2(text, () => (""));
  var size: any = py.max([1024, py.toInt(chunk_size)]);
  return py.or2(py.range(0, py.len(raw), size).map((i: any) => py.slice(raw, i, py.add(i, size))), () => ([""]));
}
