/**
 * Converted from Python: core/universal/semantic_payload_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function parseSemanticPayload(text: any): any {
  var src: any = py.or2(text, () => (""));
  var lines: any = py.iter(py.splitlines(src)).filter((ln: any) => py.truthy(py.strip(ln))).map((ln: any) => py.strip(ln));
  return {"line_count": py.len(lines), "non_empty_ratio": (!py.truthy(src) ? py.F(0.0) : py.round(py.div(py.len(py.join("\n", lines)), py.max([1, py.len(src)])), 6)), "sample": py.slice(lines, null, 20)};
}
