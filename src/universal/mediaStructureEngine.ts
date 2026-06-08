/**
 * Converted from Python: core/universal/media_structure_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function extractMediaStructure(text: any): any {
  var source: any = String(py.or2(text, () => (""))).toLowerCase();
  var media: any[] = [];
  var ext: any;
  for (ext of py.iter([".png", ".jpg", ".jpeg", ".gif", ".svg", ".mp4", ".webm", ".mp3", ".wav"])) {
    if (py.contains(source, ext)) {
      py.listAppend(media, py.lstrip(ext, "."));
    }
  }
  return {"media_types": py.sorted(py.toSet(media)), "has_media": py.truthy(media)};
}
