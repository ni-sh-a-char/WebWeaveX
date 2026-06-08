/**
 * Converted from Python: core/repository/api_surface_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { resolveApiSurface } from "../parsers/apiResolutionEngine.js";
import { ParserRegistry } from "../parsers/parserRegistry.js";

export function extractApiSurface(text: any, path: any = ""): any {
  var language: any = ParserRegistry.detect_language(path);
  var api: any = resolveApiSurface(py.or2(text, () => ("")), language, path);
  return {"routes": py.get(api, "routes", []), "rest": py.get(api, "rest", false), "graphql": py.get(api, "graphql", false), "evidence": py.get(api, "evidence", "parser_api_surface")};
}
export { ParserRegistry, resolveApiSurface };
