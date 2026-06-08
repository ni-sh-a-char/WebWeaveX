/**
 * Converted from Python: core/identity/browser_fingerprint_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import { computeKaalkaHashPayload } from "../crypto/kaalkaHashEngine.js";
import { normalizeBrowserFingerprint } from "./browserEntropyEngine.js";

export function fingerprintBrowserIdentity(identity: any): any {
  return computeKaalkaHashPayload(normalizeBrowserFingerprint(identity));
}
export { computeKaalkaHashPayload, normalizeBrowserFingerprint };
