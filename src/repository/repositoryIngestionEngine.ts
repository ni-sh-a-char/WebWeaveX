/**
 * Converted from Python: core/repository/repository_ingestion_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_FILES: any = 100000;
export let SUPPORTED_CODE_EXTENSIONS: any = new Set([".py", ".js", ".ts", ".tsx", ".jsx", ".go", ".rs", ".java", ".kt"]);
export let SKIP_DIR_NAMES: any = new Set([".git", "__pycache__", "node_modules", ".venv", "venv", "dist", "build"]);
export function ingestRepository(path: any): any {
  var root: any = py.path(path);
  if (!py.truthy(root.exists())) {
    return {"root": py.toStr(root), "files": [], "file_count": 0, "available": false, "reason": "path_not_found", "bounded": true};
  }
  var files: any[] = [];
  var count: any = 0;
  var file: any;
  for (file of py.iter(root.rglob("*"))) {
    if (py.ge(count, MAX_FILES)) {
      break;
    }
    if (!py.truthy(file.is_file())) {
      continue;
    }
    if (py.any(py.iter(file.parts).map((part: any) => py.contains(SKIP_DIR_NAMES, part)))) {
      continue;
    }
    var ext: any = String(file.suffix).toLowerCase();
    try {
      var size: any = file.stat().st_size;
    } catch (_e: any) {
      size = 0;
    }
    py.listAppend(files, {"path": py.toStr(file), "extension": ext, "supported_code": py.contains(SUPPORTED_CODE_EXTENSIONS, ext), "size": size});
    count = py.add(count, 1);
  }
  return {"root": py.toStr(root), "files": py.sorted(files, {key: ((x: any) => py.at(x, "path")) as (item: any) => any}), "file_count": py.len(files), "available": true, "bounded": true};
}
