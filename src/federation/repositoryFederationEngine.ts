/**
 * Converted from Python: core/federation/repository_federation_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function federateRepositories(repositories: any): any {
  var merged_nodes: any[] = [];
  var repo: any;
  for (repo of py.iter(repositories)) {
    py.extend(merged_nodes, py.get(repo, "nodes", []));
  }
  return {"repositories": py.len(repositories), "nodes": merged_nodes, "federated": true};
}
