/**
 * Converted from Python: core/repository/repository_intelligence.py
 * @generated — WebWeaveX python→javascript library port
 */

import { buildTopology } from "./topologyEngine.js";
import { buildDependencyGraph } from "./dependencyGraphEngine.js";
import { extractApiSurface } from "./apiSurfaceEngine.js";
import { buildImportGraph } from "./importGraphEngine.js";
import { detectPackageManagers } from "./packageEngine.js";
import { inferArchitecture } from "./architectureEngine.js";
import { classifyRepo } from "./repoClassifier.js";

export function analyzeRepository(text: any, source_url: any = ""): any {
  var topology: any = buildTopology(text);
  var dependency_graph: any = buildDependencyGraph(text);
  var api_surface: any = extractApiSurface(text);
  var import_graph: any = buildImportGraph(text);
  var packages: any = detectPackageManagers(text);
  var architecture: any = inferArchitecture(topology, import_graph);
  var classifier: any = classifyRepo(source_url);
  return {"topology": topology, "dependency_graph": dependency_graph, "api_surface": api_surface, "import_graph": import_graph, "packages": packages, "architecture": architecture, "classifier": classifier};
}
export { buildDependencyGraph, buildImportGraph, buildTopology, classifyRepo, detectPackageManagers, extractApiSurface, inferArchitecture };
