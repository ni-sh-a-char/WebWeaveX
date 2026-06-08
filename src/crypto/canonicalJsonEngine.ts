/**
 * Converted from Python: core/crypto/canonical_json_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import { dumpsDeterministic } from "../serialize/deterministicSerializer.js";

export function canonicalJson(payload: any): any {
  return dumpsDeterministic(payload);
}
export { dumpsDeterministic };
