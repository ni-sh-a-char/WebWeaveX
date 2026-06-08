/**
 * Converted from Python: core/repository/repository_api_extraction_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let ROUTE_PATTERNS: any = [py.regex("@app\\.route\\([\"\\']([^\"\\']+)", ""), py.regex("router\\.(get|post|put|delete|patch)\\([\"\\']([^\"\\']+)", ""), py.regex("@(?:get|post|put|delete|patch)\\([\"\\']([^\"\\']+)", "")];
export let MAX_ROUTES: any = 10000;
export let MAX_SOURCE_BYTES: any = 500000;
export function extractRepositoryApis(source: any): any {
  var routes: any[] = [];
  var pattern: any;
  for (pattern of py.iter(ROUTE_PATTERNS)) {
    var match: any;
    for (match of py.iter(pattern.findall(source))) {
      if ((Array.isArray(match))) {
        var route: any = py.at(match, (-1));
      } else {
        route = match;
      }
      py.listAppend(routes, py.toStr(route));
      if ((py.len(routes) >= MAX_ROUTES)) {
        break;
      }
    }
  }
  return {"routes": py.sorted(py.toSet(routes)), "bounded": true};
}
export function extractRepositoryApiIndex(files: any): any {
  var routes: any[] = [];
  var per_file: any[] = [];
  var file: any;
  for (file of py.iter(files)) {
    if (!py.eq(py.get(file, "extension"), ".py")) {
      continue;
    }
    try {
      var handle: any = py.open(py.at(file, "path"), "r");
      var source: any = handle.read(MAX_SOURCE_BYTES);
    } catch (_e: any) {
      continue;
    }
    var found: any = extractRepositoryApis(source);
    var file_routes: any = py.get(found, "routes", []);
    if (py.truthy(file_routes)) {
      py.listAppend(per_file, {"path": py.at(file, "path"), "routes": file_routes});
      py.extend(routes, file_routes);
    }
  }
  return {"routes": py.slice(py.sorted(py.toSet(routes)), null, MAX_ROUTES), "per_file": py.sorted(per_file, {key: ((x: any) => py.at(x, "path")) as (item: any) => any}), "bounded": true};
}
