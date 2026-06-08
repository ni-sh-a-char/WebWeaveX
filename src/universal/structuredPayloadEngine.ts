/**
 * Converted from Python: core/universal/structured_payload_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function extractStructuredPayload(text: any): any {
  var raw: any = py.or2(text, () => (""));
  try {
    var parsed: any = py.jsonLoads(raw);
    if (((parsed !== null && typeof parsed === "object" && !Array.isArray(parsed) && !(parsed instanceof Set) && !(parsed instanceof Map)))) {
      return {"kind": "json", "keys": py.sorted(py.keys(parsed))};
    }
    if ((Array.isArray(parsed))) {
      return {"kind": "json", "length": py.len(parsed)};
    }
  } catch (_e: any) {
  }
  if ((py.contains(raw, "<") && py.contains(raw, ">"))) {
    return {"kind": "markup", "length": py.len(raw)};
  }
  if ((py.contains(raw, ":") && py.contains(raw, "\n"))) {
    return {"kind": "key_value_text", "length": py.len(raw)};
  }
  return {"kind": "text", "length": py.len(raw)};
}
