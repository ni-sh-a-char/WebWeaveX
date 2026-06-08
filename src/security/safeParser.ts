/**
 * Converted from Python: core/security/safe_parser.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function safeHtmlText(text: any): any {
  try {
    var soup: any = py.soup(py.or2(text, () => ("")), "lxml");
    var t: any;
    for (t of py.iter(soup(["script", "style"]))) {
      t.decompose();
    }
    return soup.get_text(" ", true);
  } catch (_e: any) {
    return "";
  }
}
