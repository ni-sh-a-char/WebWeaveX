/**
 * Converted from Python: core/treesitter/language_registry.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let EXTENSION_MAP: any = {".py": "python", ".js": "javascript", ".ts": "typescript", ".tsx": "tsx", ".jsx": "jsx", ".go": "go", ".rs": "rust", ".java": "java", ".tf": "terraform", ".yaml": "yaml", ".yml": "yaml"};
export function detectLanguage(path: any): any {
  var ext: any;
  var lang: any;
  for ([ext, lang] of py.items(EXTENSION_MAP)) {
    if (py.truthy(py.endswith(path, ext))) {
      return lang;
    }
  }
  return null;
}
