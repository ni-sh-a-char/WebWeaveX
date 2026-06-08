/**
 * Converted from Python: core/repository/intelligence/repository_summary_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";

export function summarizeRepository(parts: any): any {
  return {"languages": py.sorted(py.toSet(py.get(parts, "languages", []))), "frameworks": py.sorted(py.toSet(py.get(parts, "frameworks", []))), "service_count": py.len(py.get(py.get(parts, "architecture", {}), "services", [])), "route_count": py.len(py.get(py.get(parts, "api_contract", {}), "routes", [])), "symbol_count": py.len(py.get(py.get(parts, "ast", {}), "symbols", []))};
}
