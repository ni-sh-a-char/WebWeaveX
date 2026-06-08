/**
 * Converted from Python: core/security/ssrf_guard.py
 * @generated — WebWeaveX python→javascript library port
 */

import { isSafeUrl } from "./urlValidator.js";

export function safeRemoteUrl(url: any): any {
  return isSafeUrl(url);
}
export { isSafeUrl };
