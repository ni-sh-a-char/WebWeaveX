/**
 * Converted from Python: core/identity/font_runtime_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

let _FONTS: any = {"default": ["Arial", "Courier New", "Segoe UI", "Times New Roman", "Verdana"], "profile_a": ["Arial", "Helvetica", "Menlo", "Times New Roman"], "profile_b": ["DejaVu Sans", "Liberation Sans", "Ubuntu", "Noto Sans"]};
export function buildFontRuntime(profile_id: any = "default"): any {
  var profile: any = (py.contains(_FONTS, profile_id) ? profile_id : "default");
  return {"fonts": py.sorted(py.at(_FONTS, profile)), "bounded": true};
}
