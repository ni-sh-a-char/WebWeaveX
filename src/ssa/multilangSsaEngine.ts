/**
 * Converted from Python: core/ssa/multilang_ssa_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let ASSIGNMENT_PATTERNS: any = {"python": "([a-zA-Z_][a-zA-Z0-9_]*)\\s*=", "javascript": "(?:let|const|var)\\s+([a-zA-Z_][a-zA-Z0-9_]*)", "typescript": "(?:let|const|var)\\s+([a-zA-Z_][a-zA-Z0-9_]*)"};
export function buildMultilangSsa(source: any, language: any): any {
  var pattern: any = py.get(ASSIGNMENT_PATTERNS, language);
  if ((pattern === null || pattern === undefined)) {
    return {"language": language, "variables": [], "supported": false};
  }
  var matches: any = py.reFindall(pattern, source, "");
  var counters: Record<string, any> = {};
  var variables: any[] = [];
  var name: any;
  for (name of py.iter(matches)) {
    py.setItem(counters, name, py.add(py.get(counters, name, 0), 1));
    py.listAppend(variables, {"name": name, "ssa": `${py.toStr(name)}_${py.toStr(py.at(counters, name))}`});
  }
  return {"language": language, "variables": variables, "supported": true};
}
