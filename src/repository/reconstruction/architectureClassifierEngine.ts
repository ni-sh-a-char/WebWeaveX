/**
 * Converted from Python: core/repository/reconstruction/architecture_classifier_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";

export function classifyArchitecture(topology: any, event_graph: any, deployment: any): any {
  var styles: any = ["monolith"];
  if ((py.len(py.get(topology, "services", [])) >= 5)) {
    py.listAppend(styles, "microservices");
  }
  if ((py.len(py.get(event_graph, "edges", [])) > 0)) {
    py.listAppend(styles, "event-driven");
  }
  if (py.any(py.iter(py.get(deployment, "nodes", [])).map((n: any) => py.contains(n, "kubernetes")))) {
    py.listAppend(styles, "distributed");
  }
  return {"styles": py.sorted(py.toSet(styles))};
}
