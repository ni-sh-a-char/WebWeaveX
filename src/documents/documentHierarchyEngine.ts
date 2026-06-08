/**
 * Converted from Python: core/documents/document_hierarchy_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function buildDocumentHierarchy(structure: any): any {
  var hierarchy: any[] = [];
  var sections: any = py.get(structure, "sections", []);
  var idx: any;
  var section: any;
  for ([idx, section] of py.enumerate(sections)) {
    py.listAppend(hierarchy, {"id": `section_${py.toStr(idx)}`, "title": py.get(section, "title"), "children": []});
  }
  return {"hierarchy": hierarchy, "bounded": true};
}
