/**
 * Converted from Python: core/treesitter/universal_ast_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { compileSemanticAstIr } from "../ast/index.js";
import { buildMultilangSsa } from "../ssa/multilangSsaEngine.js";
import { detectLanguage } from "./languageRegistry.js";
import { createParser } from "./treeSitterLoader.js";
import { normalizeAst } from "./universalAstNormalizer.js";

export function parseUniversalAst(source: any, path: any): any {
  var language: any = py.or2(detectLanguage(path), () => ("text"));
  var ts: any = (py.contains(new Set(["python", "javascript", "typescript", "go", "rust"]), language) ? createParser(language) : {"available": false});
  if (py.eq(language, "python")) {
    var ir: any = compileSemanticAstIr(source);
    return {"language": language, "ir": ir, "parser": "python_ast", "tree_sitter": py.get(ts, "available", false), "grounded": true};
  }
  var raw_nodes: any = py.iter(py.slice(py.splitlines(source), null, 100)).map((_: any) => ({"type": "source_line", "parent": null}));
  var normalized: any = normalizeAst(raw_nodes, language);
  var multilang: any = buildMultilangSsa(source, language);
  return {"language": language, "ir": {"normalized_ast": normalized, "multilang_ssa": multilang, "unsupported_language": !py.contains(new Set(["javascript", "typescript", "go", "rust", "python"]), language)}, "parser": (py.truthy(py.get(ts, "available")) ? "tree_sitter" : "fallback"), "tree_sitter": py.get(ts, "available", false), "grounded": py.get(multilang, "supported", false)};
}
export { buildMultilangSsa, compileSemanticAstIr, createParser, detectLanguage, normalizeAst };
