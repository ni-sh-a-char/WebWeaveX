/**
 * Converted from Python: core/repository/semantic/semantic_repository_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";
import { extractSemanticAst } from "./semanticAstEngine.js";
import { resolveSemanticSymbols } from "./semanticSymbolEngine.js";
import { buildSemanticImportGraph } from "./semanticImportEngine.js";
import { buildSemanticCallGraph } from "./semanticCallGraphEngine.js";
import { extractSemanticDependencies } from "./semanticDependencyEngine.js";
import { inferSemanticServices } from "./semanticServiceEngine.js";
import { detectSemanticRuntime } from "./semanticRuntimeEngine.js";
import { reconstructSemanticApi } from "./semanticApiEngine.js";
import { inferSemanticBuildGraph } from "./semanticBuildEngine.js";
import { detectSemanticFrameworks } from "./semanticFrameworkEngine.js";
import { reconstructSemanticArchitecture } from "./semanticArchitectureEngine.js";
import { buildSemanticRepositoryGraph } from "./semanticRepositoryGraphEngine.js";

export function extractSemanticRepository(text: any, source_url: any = ""): any {
  var src: any = py.or2(text, () => (""));
  var ast_data: any = extractSemanticAst(src);
  var symbols: any = resolveSemanticSymbols(ast_data);
  var deps: any = extractSemanticDependencies(src);
  var api: any = reconstructSemanticApi(src);
  var services: any = inferSemanticServices({"modules": []}, py.get(ast_data, "imports", []), py.get(api, "routes", []), py.get(deps, "dependencies", []));
  var runtime: any = detectSemanticRuntime(py.get(deps, "dependencies", []), py.get(deps, "package_managers", []), [source_url]);
  var frameworks: any = detectSemanticFrameworks(py.get(ast_data, "imports", []), py.get(deps, "dependencies", []), [source_url]);
  var architecture: any = reconstructSemanticArchitecture(services, py.get(deps, "dependencies", []), py.get(ast_data, "imports", []), py.get(api, "routes", []));
  var import_graph: any = buildSemanticImportGraph(ast_data, "repository");
  var call_graph: any = buildSemanticCallGraph(src);
  var build_graph: any = inferSemanticBuildGraph(py.get(deps, "package_managers", []));
  var repository_graph: any = buildSemanticRepositoryGraph({"symbols": py.get(symbols, "symbols", []), "frameworks": frameworks, "dependencies": py.get(deps, "dependencies", []), "services": py.get(services, "services", []), "routes": py.get(api, "routes", [])});
  return {"ast": ast_data, "symbols": symbols, "imports": import_graph, "calls": call_graph, "dependencies": deps, "services": services, "runtime": runtime, "api": api, "build": build_graph, "frameworks": frameworks, "architecture": architecture, "repository_graph": repository_graph};
}
export { buildSemanticCallGraph, buildSemanticImportGraph, buildSemanticRepositoryGraph, detectSemanticFrameworks, detectSemanticRuntime, extractSemanticAst, extractSemanticDependencies, inferSemanticBuildGraph, inferSemanticServices, reconstructSemanticApi, reconstructSemanticArchitecture, resolveSemanticSymbols };
