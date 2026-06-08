/**
 * Converted from Python: core/repository/async_runtime_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { parseSource } from "../parsers/parserRegistry.js";

export function detectAsyncRuntime(source: any, path: any = ""): any {
  var parsed: any = (py.truthy(source) ? parseSource(source, path) : {});
  var sym: any = (((py.get(parsed, "symbols") !== null && typeof py.get(parsed, "symbols") === "object" && !Array.isArray(py.get(parsed, "symbols")) && !(py.get(parsed, "symbols") instanceof Set) && !(py.get(parsed, "symbols") instanceof Map))) ? py.get(parsed, "symbols", {}) : {});
  var funcs: any = py.iter(py.or2(py.get(sym, "functions", []), () => ([]))).map((f: any) => py.toStr(f));
  var async_funcs: any = py.iter(funcs).filter((f: any) => (py.truthy(py.startswith(f, "async ")) || py.contains(py.or2(source, () => ("")), "async def"))).map((f: any) => f);
  var await_calls: any = py.len(py.reFindall("\\bawait\\b", py.or2(source, () => ("")), ""));
  return {"async_functions": py.slice(async_funcs, null, 50), "await_count": await_calls, "evidence": (py.truthy(funcs) ? ["parser:symbols"] : (py.truthy(await_calls) ? ["text:await"] : [])), "parser_backed": py.truthy(funcs)};
}
export { parseSource };
