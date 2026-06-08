/**
 * Converted from Python: core/identity/platform_runtime_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

let _PLATFORMS: any = {"default": "Win32", "profile_a": "MacIntel", "profile_b": "Linux x86_64"};
export function buildPlatformRuntime(profile_id: any = "default"): any {
  var profile: any = (py.contains(_PLATFORMS, profile_id) ? profile_id : "default");
  return {"platform": py.at(_PLATFORMS, profile), "bounded": true};
}
