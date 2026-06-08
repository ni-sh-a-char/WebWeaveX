/**
 * Converted from Python: core/engineering/service_dependency_pressure_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function computeDependencyPressure(graph: any): any {
  var edges: any = [...py.iter(py.get(graph, "edges", []))];
  var pressure: Record<string, any> = {};
  var edge: any;
  for (edge of py.iter(edges)) {
    var target: any = py.toStr(py.get(edge, "to"));
    py.setItem(pressure, target, py.add(py.get(pressure, target, 0), 1));
  }
  return {"dependency_pressure": py.pyDict(py.sorted(py.items(pressure)))};
}
