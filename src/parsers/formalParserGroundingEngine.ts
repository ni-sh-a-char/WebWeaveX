/**
 * Converted from Python: core/parsers/formal_parser_grounding_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let SUPPORTED: any = py.toSet(new Set(["python", "javascript", "typescript", "rust", "go", "java", "kotlin", "dart"]));
export function requireParserEvidence(parsed: any): any {
  var lang: any = String(py.toStr(py.get(parsed, "language", "text"))).toLowerCase();
  var sym: any = (((py.get(parsed, "symbols") !== null && typeof py.get(parsed, "symbols") === "object" && !Array.isArray(py.get(parsed, "symbols")) && !(py.get(parsed, "symbols") instanceof Set) && !(py.get(parsed, "symbols") instanceof Map))) ? py.get(parsed, "symbols", {}) : {});
  var flags: any = py.or2(py.get(parsed, "evidence", py.get(parsed, "parser_evidence", {})), () => ({}));
  var symbol_count: any = py.sum(py.iter(["classes", "functions", "imports", "exports", "interfaces"]).map((k: any) => py.len(py.or2(py.get(sym, k, []), () => ([])))));
  var applicable: any = py.contains(SUPPORTED, lang);
  var grounded: any = py.or2((symbol_count > 0), () => (py.truthy(flags)));
  return {"language": lang, "applicable": applicable, "grounded": (py.truthy(applicable) ? grounded : true), "symbol_count": symbol_count, "parser_required": applicable, "deterministic_inputs": [`lang=${py.toStr(lang)}`, `symbols=${py.toStr(symbol_count)}`]};
}
