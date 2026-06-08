/**
 * Converted from Python: core/repository/runtime_dependency_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function resolveRuntimeDependencies(parsed: any, text_fallback: any = ""): any {
  var deps: any[] = [];
  var evidence: any[] = [];
  if (py.truthy(parsed)) {
    var d: any = py.or2(py.get(parsed, "dependencies", {}), () => ({}));
    deps = [...py.iter(py.or2(py.get(d, "dependencies", []), () => ([])))];
    if (py.truthy(deps)) {
      py.listAppend(evidence, "parser:dependencies");
    }
    var runtime: any = py.or2(py.get(parsed, "runtime", {}), () => ({}));
    var k: any;
    for (k of py.iter(["packages", "modules"])) {
      var items: any = py.or2(py.get(runtime, k, []), () => ([]));
      if (py.truthy(items)) {
        py.extend(deps, py.iter(py.slice(items, null, 100)).map((x: any) => py.toStr(x)));
        py.listAppend(evidence, `parser:runtime_${py.toStr(k)}`);
      }
    }
  }
  if ((!py.truthy(deps) && py.truthy(text_fallback))) {
    var m: any;
    for (m of py.iter(py.reFinditer("^([A-Za-z0-9_.\\-]+)\\s*(?:==|>=)", text_fallback, "m"))) {
      py.listAppend(deps, m.group(1));
      py.listAppend(evidence, "fallback:requirements_line");
    }
  }
  return {"dependencies": py.slice(py.sorted(py.toSet(deps)), null, 200), "evidence": py.sorted(py.toSet(evidence)), "parser_first": py.truthy(py.and2(parsed, () => (py.and2(evidence, () => (py.startswith(py.at(evidence, 0), "parser"))))))};
}
