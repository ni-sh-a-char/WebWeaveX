/**
 * Converted from Python: core/treesitter/tree_sitter_loader.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

var Language: any = null;
var Parser: any = null;
var TREE_SITTER_AVAILABLE: any = false;
export let SUPPORTED_LANGUAGES: any = new Set(["python", "javascript", "typescript", "go", "rust"]);
export function createParser(language: any): any {
  if (!py.truthy(TREE_SITTER_AVAILABLE)) {
    return {"available": false, "reason": "tree_sitter_missing"};
  }
  if (!py.contains(SUPPORTED_LANGUAGES, language)) {
    return {"available": false, "reason": "unsupported_language"};
  }
  var parser: any = Parser();
  return {"available": true, "parser": parser, "language": language};
}
