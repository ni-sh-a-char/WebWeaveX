/**
 * Converted from Python: core/archive/archive_extraction_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_ARCHIVE_FILES: any = 10000;
export function extractArchive(path: any): any {
  if (!py.truthy(py.path(path).is_file())) {
    return {"files": [], "count": 0, "available": false, "reason": "file_not_found", "bounded": true};
  }
  try {
    var archive: any = py.zipFile(path);
    var names: any = py.slice(archive.namelist(), null, MAX_ARCHIVE_FILES);
    var files: any = py.iter(names).map((name: any) => ({"path": name}));
  } catch (exc: any) {
    return {"files": [], "count": 0, "available": false, "reason": py.slice(py.toStr(exc), null, 200), "bounded": true};
    /* additional except handler merged: Name(id='Exception', ctx=Load()) */
  }
  return {"files": files, "count": py.len(files), "available": true, "bounded": true};
}
