/**
 * Converted from Python: core/parsers/repository_semantic_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { ParserRegistry } from "./parserRegistry.js";
import { resolveFrameworks } from "./frameworkResolutionEngine.js";
import { resolveApiSurface } from "./apiResolutionEngine.js";
import { buildSemanticGraph } from "./semanticGraphEngine.js";

export function analyzeRepositorySource(source: any, path: any = ""): any {
  var parsed: any = ParserRegistry.parse(source, path);
  var symbols: any = py.get(parsed, "symbols", {});
  var deps: any = py.get(py.get(parsed, "dependencies", {}), "dependencies", []);
  var imports: any = py.get(symbols, "imports", []);
  var frameworks: any = resolveFrameworks(deps, imports, py.get(symbols, "decorators"));
  var api: any = resolveApiSurface(source, py.toStr(py.get(parsed, "language", "text")), path);
  py.setItem(parsed, "frameworks", frameworks);
  py.setItem(parsed, "api_surface", api);
  py.setItem(parsed, "repository_graph", buildSemanticGraph(parsed));
  return parsed;
}
export { ParserRegistry, buildSemanticGraph, resolveApiSurface, resolveFrameworks };
