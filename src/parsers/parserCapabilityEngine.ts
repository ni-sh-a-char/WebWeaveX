/**
 * Converted from Python: core/parsers/parser_capability_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let SUPPORTED: any = py.toSet(new Set(["python", "javascript", "typescript", "java", "kotlin", "dart", "rust", "go"]));
var _CAPABILITIES: any = {"python": new Set(["ast", "symbols", "imports", "calls", "decorators", "generics"]), "javascript": new Set(["tree_sitter", "symbols", "imports", "calls"]), "typescript": new Set(["tree_sitter", "symbols", "imports", "calls", "interfaces", "generics"]), "java": new Set(["tree_sitter", "symbols", "imports", "annotations"]), "kotlin": new Set(["tree_sitter", "symbols", "imports", "annotations"]), "dart": new Set(["tree_sitter", "symbols", "imports"]), "rust": new Set(["tree_sitter", "symbols", "imports", "traits"]), "go": new Set(["tree_sitter", "symbols", "imports"])};
export function languageCapabilities(language: any): any {
  var lang: any = String(py.or2(language, () => ("text"))).toLowerCase();
  var caps: any = py.get(_CAPABILITIES, lang, new Set());
  return {"language": lang, "supported": py.contains(SUPPORTED, lang), "capabilities": py.sorted(caps), "parser_backend": (py.eq(lang, "python") ? "native_ast" : "tree_sitter")};
}
