/**
 * Converted from Python: core/world_model/_normalize.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function normalizeSymbols(semantic_ast: any): any {
  var raw: any = py.get(semantic_ast, "symbols", []);
  if (((raw !== null && typeof raw === "object" && !Array.isArray(raw) && !(raw instanceof Set) && !(raw instanceof Map)))) {
    var items: any = py.get(raw, "symbols", []);
  } else if ((Array.isArray(raw))) {
    items = raw;
  } else {
    items = [];
  }
  var normalized: any[] = [];
  var item: any;
  for (item of py.iter(items)) {
    if (!((item !== null && typeof item === "object" && !Array.isArray(item) && !(item instanceof Set) && !(item instanceof Map)))) {
      continue;
    }
    var name: any = py.or2(py.get(item, "name"), () => (py.get(item, "symbol")));
    if (py.truthy(name)) {
      py.listAppend(normalized, {...(item), "name": name});
    }
  }
  return normalized;
}
export function normalizeImports(semantic_ast: any): any {
  var direct: any = py.get(semantic_ast, "imports");
  if ((Array.isArray(direct))) {
    return direct;
  }
  var ast: any = py.get(semantic_ast, "ast", {});
  if (!((ast !== null && typeof ast === "object" && !Array.isArray(ast) && !(ast instanceof Set) && !(ast instanceof Map)))) {
    return [];
  }
  var result: any[] = [];
  var imp: any;
  for (imp of py.iter(py.get(ast, "imports", []))) {
    if (!((imp !== null && typeof imp === "object" && !Array.isArray(imp) && !(imp instanceof Set) && !(imp instanceof Map)))) {
      continue;
    }
    if (py.contains(imp, "modules")) {
      var module: any;
      for (module of py.iter(py.get(imp, "modules", []))) {
        py.listAppend(result, {"module": module});
      }
    } else if (py.truthy(py.get(imp, "module"))) {
      module = py.at(imp, "module");
      var names: any = py.get(imp, "names", []);
      if (py.truthy(names)) {
        var name: any;
        for (name of py.iter(names)) {
          py.listAppend(result, {"module": `${py.toStr(module)}.${py.toStr(name)}`});
        }
      } else {
        py.listAppend(result, {"module": module});
      }
    }
  }
  return result;
}
