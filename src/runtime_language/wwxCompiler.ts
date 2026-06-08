/**
 * Converted from Python: core/runtime_language/wwx_compiler.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { validateWwx } from "./wwxValidator.js";

export function compileWwx(parsed: any): any {
  var validation: any = validateWwx(parsed);
  var plan: any = {"steps": py.iter(py.get(parsed, "statements", [])).map((stmt: any) => ({"action": String(py.at(stmt, "verb")).toLowerCase(), "target": py.at(stmt, "target"), "args": py.get(stmt, "args", [])})), "deterministic": true};
  return {"plan": plan, "validation": validation, "compiled": py.at(validation, "valid"), "bounded": true};
}
export { validateWwx };
