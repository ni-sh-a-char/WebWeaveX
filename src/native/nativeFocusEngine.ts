/**
 * Converted from Python: core/native/native_focus_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function resolveNativeFocus(windows: any, accessibility: any): any {
  var focused_window: any = py.toStr(py.get(windows, "focused_window", ""));
  var focused_control: Record<string, any> = {};
  var bucket: any;
  for (bucket of py.iter(["buttons", "text_inputs", "tabs"])) {
    var element: any;
    for (element of py.iter(py.get(accessibility, bucket, []))) {
      if (py.truthy(py.get(element, "focused"))) {
        focused_control = element;
        break;
      }
    }
    if (py.truthy(focused_control)) {
      break;
    }
  }
  return {"window": focused_window, "control": focused_control, "bounded": true};
}
