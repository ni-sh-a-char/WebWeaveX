/**
 * Converted from Python: core/repository/execution_flow_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function reconstructExecutionFlow(parsed: any): any {
  var sym: any = py.or2(py.get(py.or2(parsed, () => ({})), "symbols", {}), () => ({}));
  var funcs: any = (((sym !== null && typeof sym === "object" && !Array.isArray(sym) && !(sym instanceof Set) && !(sym instanceof Map))) ? py.get(sym, "functions", []) : []);
  var calls: any = py.or2(py.get(py.or2(py.get(py.or2(parsed, () => ({})), "calls", {}), () => ({})), "calls", []), () => ([]));
  var entrypoints: any = py.iter(funcs).filter((f: any) => py.truthy(py.startswith(py.toStr(f), ["main", "run_", "handle_"]))).map((f: any) => f);
  var flow: any = py.enumerate(py.slice(calls, null, 50)).filter(([i, c]: any) => ((c !== null && typeof c === "object" && !Array.isArray(c) && !(c instanceof Set) && !(c instanceof Map)))).map(([i, c]: any) => ({"step": i, "call": c}));
  return {"entrypoints": py.slice(entrypoints, null, 20), "flow": flow, "evidence": (py.truthy(funcs) ? ["parser:functions", "parser:call_graph"] : [])};
}
