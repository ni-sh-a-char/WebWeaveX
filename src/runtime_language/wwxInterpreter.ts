/**
 * Converted from Python: core/runtime_language/wwx_interpreter.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { compileWwx } from "./wwxCompiler.js";
import { parseWwx } from "./wwxParser.js";

export function interpretWwx(source: any, tick: any = 0): any {
  var parsed: any = parseWwx(source);
  var compiled: any = compileWwx(parsed);
  var results: any[] = [];
  var step: any;
  for (step of py.iter(py.get(py.get(compiled, "plan", {}), "steps", []))) {
    py.listAppend(results, {"action": py.at(step, "action"), "target": py.at(step, "target"), "simulated": py.contains(["extract", "sync", "replay"], py.at(step, "action")), "tick": tick, "executed": py.eq(py.at(step, "action"), "execute")});
  }
  return {"parsed": parsed, "compiled": compiled, "results": results, "deterministic": true, "bounded": true};
}
export { compileWwx, parseWwx };
