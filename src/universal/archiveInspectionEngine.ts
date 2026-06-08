/**
 * Converted from Python: core/universal/archive_inspection_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function inspectArchive(name_or_text: any): any {
  var src: any = String(py.or2(name_or_text, () => (""))).toLowerCase();
  var formats: any = py.iter([".zip", ".tar", ".tgz", ".gz", ".rar", ".7z"]).filter((ext: any) => py.contains(src, ext)).map((ext: any) => ext);
  return {"is_archive": py.truthy(formats), "formats": py.sorted(py.toSet(formats))};
}
