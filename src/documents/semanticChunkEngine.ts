/**
 * Converted from Python: core/documents/semantic_chunk_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function buildSemanticChunks(text: any, chunk_size: any = 1200): any {
  var src: any = py.or2(text, () => (""));
  var chunks: any = py.or2(py.range(0, py.len(src), chunk_size).map((i: any) => py.slice(src, i, py.add(i, chunk_size))), () => ([""]));
  return {"chunks": chunks, "chunk_ids": py.range(py.len(chunks)).map((i: any) => `chunk_${py.format(i, `04d`)}`)};
}
