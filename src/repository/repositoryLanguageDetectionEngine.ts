/**
 * Converted from Python: core/repository/repository_language_detection_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let EXTENSION_LANGUAGE_MAP: any = {".py": "python", ".js": "javascript", ".ts": "typescript", ".tsx": "typescript", ".jsx": "javascript", ".go": "go", ".rs": "rust", ".java": "java", ".kt": "kotlin"};
export function detectRepositoryLanguages(files: any): any {
  var counts: any = py.counter();
  var file: any;
  for (file of py.iter(files)) {
    var ext: any = py.get(file, "extension");
    var language: any = py.get(EXTENSION_LANGUAGE_MAP, ext);
    if (py.truthy(language)) {
      py.setItem(counts, language, py.add(py.at(counts, language), 1));
    }
  }
  return {"languages": py.pyDict(py.sorted(py.items(counts))), "primary_language": (py.truthy(counts) ? py.at(py.at(py.mostCommon(counts, 1), 0), 0) : null), "bounded": true};
}
