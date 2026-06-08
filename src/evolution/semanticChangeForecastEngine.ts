/**
 * Converted from Python: core/evolution/semantic_change_forecast_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function forecastSemanticChange(changes: any): any {
  var ordered: any = py.sorted(changes, {key: ((x: any) => py.toStr(py.get(x, "id"))) as (item: any) => any});
  return {"forecast": ordered, "forecast_size": py.len(ordered)};
}
