/**
 * Converted from Python: core/universal/universal_parser_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { detectProtocolIntelligence } from "./protocolIntelligenceEngine.js";
import { extractStructuredPayload } from "./structuredPayloadEngine.js";

export function parseUniversalPayload(text: any, source_url: any = ""): any {
  var raw: any = py.or2(text, () => (""));
  var payload: any = extractStructuredPayload(raw);
  return {"source_url": source_url, "protocol": detectProtocolIntelligence(source_url), "structured": payload, "length": py.len(raw)};
}
export { detectProtocolIntelligence, extractStructuredPayload };
