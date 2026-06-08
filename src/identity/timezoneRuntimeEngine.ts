/**
 * Converted from Python: core/identity/timezone_runtime_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

let _TIMEZONES: any = {"default": "America/New_York", "profile_a": "Europe/London", "profile_b": "America/Los_Angeles"};
export function buildTimezoneRuntime(profile_id: any = "default"): any {
  var profile: any = (py.contains(_TIMEZONES, profile_id) ? profile_id : "default");
  return {"timezone": py.at(_TIMEZONES, profile), "bounded": true};
}
