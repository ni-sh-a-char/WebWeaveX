/**
 * Converted from Python: core/streaming/streaming_pipeline.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { extract } from "../extract/pipeline.js";
import { incrementalExtract } from "./incrementalExtractor.js";

export function streamExtract(input_data: any): any {
  var text: any = ((typeof input_data === "string") ? input_data : py.toStr(input_data));
  var inc: any = incrementalExtract(text);
  var out: any = extract(text);
  py.setItem(py.at(out, "metadata"), "streaming", {"chunk_count": py.len(py.at(inc, "chunks")), "chunk_order": py.at(inc, "chunk_order")});
  return out;
}
export { extract, incrementalExtract };
