/**
 * Converted from Python: core/repository/repository_reconstruction_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { parseSource } from "../parsers/index.js";
import { buildDependencyLineage, buildDeploymentGraph, buildEventGraph, buildRuntimeGraph, classifyArchitecture, inferOwnershipDomains, reconstructMonorepo, reconstructTopology } from "./reconstruction/index.js";

export function reconstructRepository(text: any, source_url: any = "", paths: any = null): any {
  var parsed: any = parseSource(text, py.or2(source_url, () => ("repository")));
  var path_list: any = ((Array.isArray(paths)) ? paths : []);
  var topology: any = reconstructTopology(path_list);
  var events: any = buildEventGraph(text);
  var runtime: any = buildRuntimeGraph(py.get(py.get(parsed, "runtime", {}), "runtimes", []), py.get(topology, "services", []));
  var deployment: any = buildDeploymentGraph(text);
  return {"parser": parsed, "topology": topology, "events": events, "runtime_graph": runtime, "deployment": deployment, "architecture": classifyArchitecture(topology, events, deployment), "monorepo": reconstructMonorepo(path_list), "ownership": inferOwnershipDomains(path_list), "dependency_lineage": buildDependencyLineage(py.get(py.get(parsed, "dependencies", {}), "dependencies", []))};
}
export { buildDependencyLineage, buildDeploymentGraph, buildEventGraph, buildRuntimeGraph, classifyArchitecture, inferOwnershipDomains, parseSource, reconstructMonorepo, reconstructTopology };
