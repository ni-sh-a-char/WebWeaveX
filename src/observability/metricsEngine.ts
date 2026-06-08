/**
 * Converted from Python: core/observability/metrics_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function performanceMetrics(durations_ms: any): any {
  var items: any = py.sorted(py.items(py.or2(durations_ms, () => ({}))));
  var total: any = py.sum(py.iter(items).map(([_, v]: any) => v));
  return {"total_ms": total, "breakdown": items};
}
