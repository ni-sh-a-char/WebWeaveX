/**
 * Converted from Python: core/documents/document_structure_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_SECTIONS: any = 5000;
export let HEADING_PREFIXES: any = ["#", "##", "###"];
export function buildDocumentStructure(text: any): any {
  var sections: any[] = [];
  var current: any = {"title": "root", "content": []};
  var lines: any = py.splitlines(text);
  var line: any;
  for (line of py.iter(py.slice(lines, null, MAX_SECTIONS))) {
    var stripped: any = py.strip(line);
    if (py.truthy(py.startswith(stripped, HEADING_PREFIXES))) {
      if (py.truthy(py.at(current, "content"))) {
        py.listAppend(sections, current);
      }
      current = {"title": py.strip(py.lstrip(stripped, "#")), "content": []};
    } else {
      py.listAppend(py.at(current, "content"), stripped);
    }
  }
  if (py.truthy(py.at(current, "content"))) {
    py.listAppend(sections, current);
  }
  return {"sections": sections, "bounded": true};
}
