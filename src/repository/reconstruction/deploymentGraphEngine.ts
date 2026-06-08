/**
 * Converted from Python: core/repository/reconstruction/deployment_graph_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";

export function buildDeploymentGraph(text: any): any {
  var src: any = String(py.or2(text, () => (""))).toLowerCase();
  var nodes: any[] = [];
  var k: any;
  for (k of py.iter(["docker", "kubernetes", "helm", "terraform", "github actions", "gitlab-ci"])) {
    if (py.contains(src, k)) {
      py.listAppend(nodes, k);
    }
  }
  var n: any = py.sorted(py.toSet(nodes));
  var edges: any = py.range(py.max([0, py.sub(py.len(n), 1)])).map((i: any) => ({"from": py.at(n, i), "to": py.at(n, py.add(i, 1))}));
  return {"nodes": n, "edges": edges};
}
