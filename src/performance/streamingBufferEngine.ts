/**
 * Converted from Python: core/performance/streaming_buffer_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function boundedChunks(text: any, chunk_size: any = 4096): any {
  var src: any = py.or2(text, () => (""));
  return py.or2(py.range(0, py.len(src), chunk_size).map((i: any) => py.slice(src, i, py.add(i, chunk_size))), () => ([""]));
}
