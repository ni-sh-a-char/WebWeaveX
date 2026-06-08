/**
 * Converted from Python: core/parsers/framework_resolution_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

let _FRAMEWORK_DEPS: any = new Set(["django", "flask", "fastapi", "react", "next", "express", "spring-boot", "spring", "flutter", "gin", "actix", "tokio"]);
export function resolveFrameworks(dependencies: any, imports: any, decorators: any = null): any {
  var deps: any = py.toSet(py.iter(py.or2(dependencies, () => ([]))).map((d: any) => String(d).toLowerCase()));
  var imps: any = String(py.join(" ", py.or2(imports, () => ([])))).toLowerCase();
  var decs: any = py.toSet(py.iter(py.or2(decorators, () => ([]))).map((d: any) => String(d).toLowerCase()));
  var detected: any = py.sorted(py.iter(_FRAMEWORK_DEPS).filter((fw: any) => (py.contains(deps, fw) || py.contains(imps, fw) || py.contains(decs, fw) || py.any(py.iter(py.split(imps)).map((i: any) => py.contains(i, fw))))).map((fw: any) => fw));
  return {"frameworks": detected, "indicators": py.sorted(py.bitand(deps, _FRAMEWORK_DEPS))};
}
