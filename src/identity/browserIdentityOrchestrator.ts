/**
 * Converted from Python: core/identity/browser_identity_orchestrator.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { computeRuntimeEntropy, normalizeBrowserFingerprint } from "./browserEntropyEngine.js";
import { fingerprintBrowserIdentity } from "./browserFingerprintEngine.js";
import { buildBrowserProfile } from "./browserProfileEngine.js";
import { buildCanvasRuntime } from "./canvasRuntimeEngine.js";
import { buildFontRuntime } from "./fontRuntimeEngine.js";
import { buildLanguageRuntime } from "./languageRuntimeEngine.js";
import { buildMediaDeviceRuntime } from "./mediaDeviceRuntimeEngine.js";
import { buildNavigatorRuntime } from "./navigatorRuntimeEngine.js";
import { buildPlatformRuntime } from "./platformRuntimeEngine.js";
import { buildTimezoneRuntime } from "./timezoneRuntimeEngine.js";
import { buildUserAgentRuntime } from "./userAgentRuntimeEngine.js";
import { buildWebglRuntime } from "./webglRuntimeEngine.js";

let _SCREEN_PROFILES: any = {"default": {"width": 1920, "height": 1080, "colorDepth": 24}, "profile_a": {"width": 1440, "height": 900, "colorDepth": 24}, "profile_b": {"width": 2560, "height": 1440, "colorDepth": 24}};
export function buildBrowserIdentity(profile_id: any = "default"): any {
  var profile: any = buildBrowserProfile(profile_id);
  var bounded_id: any = py.at(profile, "profile_id");
  var ua: any = buildUserAgentRuntime(bounded_id);
  var platform: any = buildPlatformRuntime(bounded_id);
  var languages: any = buildLanguageRuntime(bounded_id);
  var timezone: any = buildTimezoneRuntime(bounded_id);
  var webgl: any = buildWebglRuntime(bounded_id);
  var canvas: any = buildCanvasRuntime(bounded_id);
  var fonts: any = buildFontRuntime(bounded_id);
  var media: any = buildMediaDeviceRuntime(bounded_id);
  var navigator: any = buildNavigatorRuntime(bounded_id);
  var identity: any = {"profile_id": bounded_id, "user_agent": py.at(ua, "user_agent"), "platform": py.at(platform, "platform"), "languages": py.at(languages, "languages"), "timezone": py.at(timezone, "timezone"), "screen": py.pyDict(py.get(_SCREEN_PROFILES, bounded_id, py.at(_SCREEN_PROFILES, "default"))), "webgl": webgl, "fonts": py.at(fonts, "fonts"), "media_devices": {"audio_inputs": py.at(media, "audio_inputs"), "video_inputs": py.at(media, "video_inputs"), "audio_outputs": py.at(media, "audio_outputs")}, "canvas_fingerprint": py.at(canvas, "canvas_fingerprint"), "navigator": navigator, "rotation_index": py.get(profile, "rotation_index", 0), "bounded": true};
  var entropy: any = computeRuntimeEntropy(identity);
  py.setItem(identity, "entropy_profile", py.at(entropy, "baseline_hash"));
  py.setItem(identity, "fingerprint_hash", fingerprintBrowserIdentity(identity));
  return identity;
}
export { buildBrowserProfile, buildCanvasRuntime, buildFontRuntime, buildLanguageRuntime, buildMediaDeviceRuntime, buildNavigatorRuntime, buildPlatformRuntime, buildTimezoneRuntime, buildUserAgentRuntime, buildWebglRuntime, computeRuntimeEntropy, fingerprintBrowserIdentity, normalizeBrowserFingerprint };
