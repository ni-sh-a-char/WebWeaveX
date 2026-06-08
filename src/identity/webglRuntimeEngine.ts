/**
 * Converted from Python: core/identity/webgl_runtime_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

let _WEBGL: any = {"default": {"vendor": "Google Inc. (Intel)", "renderer": "ANGLE (Intel, Intel(R) UHD Graphics Direct3D11 vs_5_0 ps_5_0)", "extensions": ["WEBGL_debug_renderer_info", "OES_texture_float"]}, "profile_a": {"vendor": "Apple Inc.", "renderer": "Apple GPU", "extensions": ["WEBGL_debug_renderer_info"]}, "profile_b": {"vendor": "Google Inc. (NVIDIA)", "renderer": "ANGLE (NVIDIA, NVIDIA GeForce GTX 1060)", "extensions": ["WEBGL_debug_renderer_info", "EXT_texture_filter_anisotropic"]}};
export function buildWebglRuntime(profile_id: any = "default"): any {
  var profile: any = (py.contains(_WEBGL, profile_id) ? profile_id : "default");
  var data: any = py.at(_WEBGL, profile);
  return {"vendor": py.at(data, "vendor"), "renderer": py.at(data, "renderer"), "extensions": py.sorted(py.at(data, "extensions")), "bounded": true};
}
