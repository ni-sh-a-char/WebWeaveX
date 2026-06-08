/**
 * Converted from Python: core/repository/repository_dependency_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let IMPORT_RE: any = py.regex("^\\s*(?:import|from)\\s+([a-zA-Z0-9_\\.]+)", "m");
export let MAX_IMPORTS: any = 10000;
export let MAX_SOURCE_BYTES: any = 500000;
export function extractDependencies(source: any): any {
  var imports: any[] = [];
  var match: any;
  for (match of py.iter(IMPORT_RE.findall(source))) {
    py.listAppend(imports, match);
    if ((py.len(imports) >= MAX_IMPORTS)) {
      break;
    }
  }
  return {"imports": py.sorted(py.toSet(imports)), "bounded": true};
}
export function extractRepositoryDependencies(files: any): any {
  var all_imports: any[] = [];
  var per_file: any[] = [];
  var edges: any[] = [];
  var file: any;
  for (file of py.iter(files)) {
    if (!py.truthy(py.get(file, "supported_code"))) {
      continue;
    }
    try {
      var handle: any = py.open(py.at(file, "path"), "r");
      var source: any = handle.read(MAX_SOURCE_BYTES);
    } catch (_e: any) {
      continue;
    }
    var deps: any = extractDependencies(source);
    var imports: any = py.get(deps, "imports", []);
    py.listAppend(per_file, {"path": py.at(file, "path"), "imports": imports});
    py.extend(all_imports, imports);
    var imp: any;
    for (imp of py.iter(imports)) {
      py.listAppend(edges, {"from": py.at(file, "path"), "to": imp, "relation": "imports"});
    }
  }
  return {"imports": py.slice(py.sorted(py.toSet(all_imports)), null, MAX_IMPORTS), "per_file": py.sorted(per_file, {key: ((x: any) => py.at(x, "path")) as (item: any) => any}), "edges": py.sorted(py.slice(edges, null, MAX_IMPORTS), {key: ((x: any) => [py.toStr(py.get(x, "from")), py.toStr(py.get(x, "to"))]) as (item: any) => any}), "bounded": true};
}
