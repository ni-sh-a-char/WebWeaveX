/**
 * Converted from Python: core/universal/archive_intelligence_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function extractArchiveIntelligence(path_or_text: any): any {
  var source: any = String(py.or2(path_or_text, () => (""))).toLowerCase();
  var formats: any[] = [];
  var ext: any;
  for (ext of py.iter([".zip", ".tar", ".gz", ".tgz", ".rar", ".7z"])) {
    if (py.contains(source, ext)) {
      py.listAppend(formats, py.lstrip(ext, "."));
    }
  }
  return {"archive_formats": py.sorted(py.toSet(formats)), "is_archive": py.truthy(formats)};
}
