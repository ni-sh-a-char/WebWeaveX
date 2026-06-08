/**
 * Converted from Python: core/parsers/runtime_resolution_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

let _FRAMEWORK_HINTS: any = {"python": new Set(["django", "flask", "fastapi", "uvicorn", "celery"]), "node": new Set(["react", "next", "express", "nestjs", "@angular/core"]), "jvm": new Set(["spring-boot", "spring", "kotlin"]), "rust": new Set(["tokio", "actix-web"]), "go": new Set(["gin", "echo"]), "dart": new Set(["flutter"])};
export function resolveRuntime(dependencies: any, imports: any): any {
  var deps: any = py.toSet(py.iter(py.or2(dependencies, () => ([]))).map((d: any) => String(d).toLowerCase()));
  var imps: any = py.toSet(py.iter(py.or2(imports, () => ([]))).map((i: any) => String(i).toLowerCase()));
  var runtimes: Set<any> = new Set();
  var frameworks: Set<any> = new Set();
  var api_indicators: Set<any> = new Set();
  var runtime: any;
  var hints: any;
  for ([runtime, hints] of py.items(_FRAMEWORK_HINTS)) {
    if ((py.truthy(py.bitand(deps, hints)) || py.any(py.iter(imps).map((i: any) => py.any(py.iter(hints).map((h: any) => py.contains(i, h))))))) {
      py.setAdd(runtimes, runtime);
      py.update(frameworks, py.sorted(py.bitand(deps, hints)));
    }
  }
  if (py.any(py.iter(imps).map((i: any) => py.or2(py.startswith(i, "python"), () => (py.endswith(i, ".py")))))) {
    py.setAdd(runtimes, "python");
  }
  if ((py.contains(deps, "fastapi") || py.contains(deps, "flask") || py.contains(deps, "django"))) {
    py.setAdd(api_indicators, "http_api");
  }
  if (py.contains(deps, "graphql")) {
    py.setAdd(api_indicators, "graphql");
  }
  return {"runtimes": py.sorted(runtimes), "frameworks": py.sorted(frameworks), "api_indicators": py.sorted(api_indicators)};
}
