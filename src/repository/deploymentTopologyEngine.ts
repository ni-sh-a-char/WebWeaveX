/**
 * Converted from Python: core/repository/deployment_topology_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { buildTopologyCognition } from "./topologyCognitionEngine.js";

export function inferDeploymentTopology(text: any): any {
  var src: any = py.or2(text, () => (""));
  var targets: any[] = [];
  var pat: any;
  for (pat of py.iter(["image:\\s*([^\\s]+)", "container_name:\\s*([^\\s]+)", "deployment\\.kubernetes\\.io/([^\\s]+)", "helm\\s+install\\s+([^\\s]+)"])) {
    py.extend(targets, py.reFindall(pat, src, "i"));
  }
  var observed_nodes: any = py.sorted(py.toSet(targets));
  var cognition: any = buildTopologyCognition(text, "deploy.yaml", observed_nodes, observed_nodes);
  py.setItem(cognition, "deployments", observed_nodes);
  py.setItem(cognition, "evidence", py.sorted(py.toSet(py.add(py.or2(py.get(cognition, "evidence"), () => ([])), ["manifest_patterns"]))));
  return cognition;
}
export { buildTopologyCognition };
