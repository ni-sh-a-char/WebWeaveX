/**
 * Converted from Python: core/repository/api_surface_reasoning_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function reasonApiSurface(spec: any): any {
  var paths: any = (((spec !== null && typeof spec === "object" && !Array.isArray(spec) && !(spec instanceof Set) && !(spec instanceof Map))) ? py.get(spec, "paths", {}) : {});
  if (!((paths !== null && typeof paths === "object" && !Array.isArray(paths) && !(paths instanceof Set) && !(paths instanceof Map)))) {
    paths = {};
  }
  var endpoints: any[] = [];
  var path: any;
  var methods: any;
  for ([path, methods] of py.items(paths)) {
    if (((methods !== null && typeof methods === "object" && !Array.isArray(methods) && !(methods instanceof Set) && !(methods instanceof Map)))) {
      var method: any;
      for (method of py.iter(methods)) {
        py.listAppend(endpoints, {"path": path, "method": String(method).toUpperCase()});
      }
    }
  }
  return {"paths": endpoints, "path_count": py.len(endpoints), "evidence": (py.truthy(endpoints) ? ["openapi:paths"] : []), "deterministic_inputs": [`paths=${py.toStr(py.len(endpoints))}`]};
}
