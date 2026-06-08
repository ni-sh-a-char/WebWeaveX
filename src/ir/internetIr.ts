/**
 * Converted from Python: core/ir/internet_ir.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { computeProbabilisticTrust } from "../internet/probabilisticTrustEngine.js";
import { emptyConfidence, emptyLineage } from "./_base.js";

export let InternetIR: any = py.at(Object, [py.toStr, Object]);
export function compileInternetIr(url: any, html: any = "", claims: any = null): any {
  var trust: any = computeProbabilisticTrust(url, 0, html, claims);
  return {"url": url, "trust": trust, "evidence": py.get(trust, "evidence", []), "lineage": emptyLineage("internet_ir"), "confidence": {"score": py.get(trust, "trust_score", 0), "basis": py.get(trust, "deterministic_inputs", []), "deterministic": true}};
}
export { computeProbabilisticTrust, emptyConfidence, emptyLineage };
