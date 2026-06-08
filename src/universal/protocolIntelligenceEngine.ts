/**
 * Converted from Python: core/universal/protocol_intelligence_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function detectProtocolIntelligence(source: any): any {
  var p: any = py.urlparse(py.or2(source, () => ("")));
  var scheme: any = String(py.or2(p.scheme, () => ("unknown"))).toLowerCase();
  var host: any = String(py.or2(p.netloc, () => (""))).toLowerCase();
  return {"scheme": scheme, "host": host};
}
