/**
 * Converted from Python: core/identity/navigator_runtime_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { buildLanguageRuntime } from "./languageRuntimeEngine.js";
import { buildPlatformRuntime } from "./platformRuntimeEngine.js";
import { buildUserAgentRuntime } from "./userAgentRuntimeEngine.js";

export function buildNavigatorRuntime(profile_id: any = "default"): any {
  var ua: any = buildUserAgentRuntime(profile_id);
  var platform: any = buildPlatformRuntime(profile_id);
  var languages: any = buildLanguageRuntime(profile_id);
  return {"webdriver": false, "plugins": ["Chrome PDF Plugin", "Chrome PDF Viewer"], "mimeTypes": ["application/pdf"], "hardwareConcurrency": 8, "deviceMemory": 8, "languages": py.at(languages, "languages"), "permissions": {"notifications": "default", "geolocation": "prompt"}, "user_agent": py.at(ua, "user_agent"), "platform": py.at(platform, "platform"), "bounded": true};
}
export { buildLanguageRuntime, buildPlatformRuntime, buildUserAgentRuntime };
