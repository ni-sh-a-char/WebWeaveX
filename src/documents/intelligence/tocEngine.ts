/**
 * Converted from Python: core/documents/intelligence/toc_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";
import { extractHeadings } from "../headingEngine.js";

export function buildToc(text: any): any {
  var heads: any = py.get(extractHeadings(text), "headings", []);
  return {"toc": py.iter(heads).map((h: any) => ({"title": py.get(h, "title", ""), "level": py.get(h, "level", 1)}))};
}
export { extractHeadings };
