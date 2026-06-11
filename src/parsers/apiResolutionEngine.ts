/**
 * Converted from Python: core/parsers/api_resolution_engine.py
 * Hand-fixed production module (protected): Python's two-group re.findall
 * yields TUPLES whose str() renders as "('get', '/users')"; the generated
 * array repr diverged. The tuple repr is now produced explicitly.
 */

import * as py from "../runtime/pyCompat.js";
import { resolveSymbols } from "./symbolResolutionEngine.js";

export function resolveApiSurface(source: any, language: any, path: any = ""): any {
  var symbols: any = resolveSymbols(source, language);
  var routes: any[] = [];
  var dec: any;
  for (dec of py.iter(py.get(symbols, "decorators", []))) {
    if (py.contains(new Set(["get", "post", "put", "delete", "patch", "route"]), dec)) {
      py.listAppend(routes, dec);
    }
  }
  for (const pair of py.reFindall("@(?:app|router)\\.(get|post|put|delete|patch)\\(['\\\"]([^'\\\"]+)", py.or2(source, () => ("")), "")) {
    // CPython tuple repr for the two-group match
    routes.push(`('${pair[0]}', '${pair[1]}')`);
  }
  py.extend(routes, py.reFindall("\\b(?:GET|POST|PUT|DELETE|PATCH)\\s+(/[^\\s'\\\"]+)", py.or2(source, () => ("")), ""));
  var graphql: any = py.contains(String(py.or2(source, () => (""))).toLowerCase(), "graphql");
  return {"routes": py.sorted(py.toSet(py.iter(routes).filter((r: any) => py.truthy(r)).map((r: any) => py.toStr(r)))), "graphql": graphql, "rest": py.truthy(routes), "evidence": "parser_symbols_and_patterns"};
}
export { resolveSymbols };
