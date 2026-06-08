/**
 * Converted from Python: core/native/native_clipboard_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function captureNativeClipboard(snapshot: any = null): any {
  var snap: any = py.or2(snapshot, () => ({}));
  return {"text": py.toStr(py.get(snap, "text", "")), "formats": [...py.iter(py.get(snap, "formats", []))], "available": py.truthy(py.get(snap, "text")), "bounded": true};
}
