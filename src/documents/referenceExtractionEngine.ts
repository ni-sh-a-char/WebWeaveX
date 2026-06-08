/**
 * Converted from Python: core/documents/reference_extraction_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let REFERENCE_SECTIONS: any = new Set(["references", "bibliography"]);
export function extractReferences(structure: any): any {
  var references: any[] = [];
  var section: any;
  for (section of py.iter(py.get(structure, "sections", []))) {
    var title: any = String(py.strip(py.get(section, "title", ""))).toLowerCase();
    if (py.contains(REFERENCE_SECTIONS, title)) {
      py.extend(references, py.get(section, "content", []));
    }
  }
  return {"references": references, "bounded": true};
}
