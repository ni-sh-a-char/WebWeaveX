/**
 * Converted from Python: core/identity/user_agent_runtime_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

let _USER_AGENTS: any = {"default": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36", "profile_a": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36", "profile_b": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"};
export function buildUserAgentRuntime(profile_id: any = "default"): any {
  var profile: any = (py.contains(_USER_AGENTS, profile_id) ? profile_id : "default");
  return {"user_agent": py.at(_USER_AGENTS, profile), "bounded": true};
}
