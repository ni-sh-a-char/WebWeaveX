/**
 * Converted from Python: core/ir/repository_runtime_ir.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function compileRepositoryRuntimeIr(ingestion: any, languages: any, graph: any, services: any, infra: any, topology: any, dependencies: any = null, apis: any = null, execution_flows: any = null, build_systems: any = null): any {
  var deps: any = py.or2(dependencies, () => ({}));
  var api_index: any = py.or2(apis, () => ({}));
  var flows: any = py.or2(execution_flows, () => ({}));
  var builds: any = py.or2(build_systems, () => ({}));
  return {"ir": "repository_runtime", "ingestion": ingestion, "languages": languages, "graph": graph, "services": py.get(services, "services", []), "dependencies": py.get(deps, "imports", []), "dependency_edges": py.get(deps, "edges", []), "apis": py.get(api_index, "routes", []), "api_index": py.get(api_index, "per_file", []), "execution_flows": py.get(flows, "flows", []), "infra": py.get(infra, "infra", []), "deployments": py.iter(py.get(infra, "infra", [])).filter((item: any) => py.contains(new Set(["kubernetes", "docker-compose", "docker"]), py.get(item, "type"))).map((item: any) => item), "runtime_topology": topology, "build_systems": py.get(builds, "build_systems", []), "bounded": true};
}
