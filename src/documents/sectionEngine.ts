/**
 * Converted from Python: core/documents/section_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { extractHeadings } from "./headingEngine.js";

export function extractSections(text: any): any {
  var heads: any = py.get(extractHeadings(text), "headings", []);
  var sections: any = py.iter(heads).map((h: any) => py.get(h, "title", ""));
  var hierarchy: any = py.iter(heads).map((h: any) => ({"title": py.get(h, "title", ""), "level": py.get(h, "level", 1)}));
  return {"sections": py.sorted(py.toSet(sections)), "hierarchy": hierarchy};
}
export { extractHeadings };
