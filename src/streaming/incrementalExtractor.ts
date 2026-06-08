/**
 * Converted from Python: core/streaming/incremental_extractor.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { parseStream } from "./streamParser.js";

export function incrementalExtract(text: any): any {
  var parsed: any = parseStream(text);
  return {"chunks": py.iter(py.at(parsed, "chunks")).map((c: any) => ({"id": py.at(c, "id"), "length": py.len(py.at(c, "text"))})), "chunk_order": py.at(parsed, "chunk_order")};
}
export { parseStream };
