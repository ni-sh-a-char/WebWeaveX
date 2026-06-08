/**
 * Converted from Python: core/repository/kubernetes_semantic_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function _parseKubernetesLines(text: any): any {
  var workloads: any[] = [];
  var kind: any = null;
  var name: any = null;
  var in_metadata: any = false;
  var line: any;
  for (line of py.iter(py.splitlines(text))) {
    var stripped: any = py.strip(line);
    if (py.truthy(py.startswith(stripped, "kind:"))) {
      if (py.truthy(kind)) {
        py.listAppend(workloads, {"kind": kind, "name": name});
      }
      kind = py.strip(py.at(py.split(stripped, ":", 1), 1));
      name = null;
      in_metadata = false;
    } else if (py.eq(stripped, "metadata:")) {
      in_metadata = true;
    } else if ((py.truthy(in_metadata) && py.truthy(py.startswith(stripped, "name:")))) {
      name = py.strip(py.at(py.split(stripped, ":", 1), 1));
      in_metadata = false;
    }
  }
  if (py.truthy(kind)) {
    py.listAppend(workloads, {"kind": kind, "name": name});
  }
  return workloads;
}
export function parseKubernetesSemantics(text: any): any {
  var workloads: any[] = [];
  var yaml: any = null;
  workloads = _parseKubernetesLines(text);
  return {"workloads": workloads, "count": py.len(workloads), "grounded": true, "deterministic": true};
}
