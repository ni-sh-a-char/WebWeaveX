/**
 * Converted from Python: core/repository/universal_repository_extraction_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { ingestRepository } from "./repositoryIngestionEngine.js";
import { detectRepositoryLanguages } from "./repositoryLanguageDetectionEngine.js";
import { buildRepositoryFileGraph } from "./repositoryFileGraphEngine.js";
import { extractRepositoryDependencies } from "./repositoryDependencyEngine.js";
import { detectRepositoryServices } from "./repositoryServiceDetectionEngine.js";
import { extractRepositoryApiIndex } from "./repositoryApiExtractionEngine.js";
import { detectRepositoryInfra } from "./repositoryInfraDetectionEngine.js";
import { reconstructExecutionFlows } from "./repositoryExecutionFlowEngine.js";
import { buildRuntimeTopology } from "./repositoryRuntimeTopologyEngine.js";
import { detectBuildSystems } from "./repositoryBuildSystemEngine.js";
import { compileRepositoryRuntimeIr } from "../ir/repositoryRuntimeIr.js";

export function extractRepository(path: any): any {
  var ingestion: any = ingestRepository(path);
  if (!py.truthy(py.get(ingestion, "available", true))) {
    return {"repository_ir": {"ir": "repository_runtime", "available": false, "reason": py.get(ingestion, "reason")}, "bounded": true};
  }
  var files: any = py.at(ingestion, "files");
  var languages: any = detectRepositoryLanguages(files);
  var dependencies: any = extractRepositoryDependencies(files);
  var graph: any = buildRepositoryFileGraph(files, py.get(dependencies, "edges", []));
  var services: any = detectRepositoryServices(files);
  var apis: any = extractRepositoryApiIndex(files);
  var infra: any = detectRepositoryInfra(files);
  var build_systems: any = detectBuildSystems(files);
  var execution_flows: any = reconstructExecutionFlows(dependencies);
  var topology: any = buildRuntimeTopology(services, infra);
  var repository_ir: any = compileRepositoryRuntimeIr(ingestion, languages, graph, services, infra, topology, dependencies, apis, execution_flows, build_systems);
  return {"ingestion": ingestion, "languages": languages, "dependencies": dependencies, "graph": graph, "services": services, "apis": apis, "infra": infra, "build_systems": build_systems, "execution_flows": execution_flows, "runtime_topology": topology, "repository_ir": repository_ir, "bounded": true};
}
export { buildRepositoryFileGraph, buildRuntimeTopology, compileRepositoryRuntimeIr, detectBuildSystems, detectRepositoryInfra, detectRepositoryLanguages, detectRepositoryServices, extractRepositoryApiIndex, extractRepositoryDependencies, ingestRepository, reconstructExecutionFlows };
