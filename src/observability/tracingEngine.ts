/**
 * Converted from Python: core/observability/tracing_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function deterministicTrace(seed: any): any {
  var s: any = py.or2(seed, () => ("webweavex"));
  return {"trace_id": py.slice(py.hashNew("sha256", py.encode(s, "utf-8")).hexdigest(), null, 32)};
}
