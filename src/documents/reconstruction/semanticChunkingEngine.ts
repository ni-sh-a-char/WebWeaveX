/**
 * Converted from Python: core/documents/reconstruction/semantic_chunking_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";

export function chunkSemantic(text: any, chunk_size: any = 1500): any {
  var src: any = py.or2(text, () => (""));
  var chunks: any = py.or2(py.range(0, py.len(src), chunk_size).map((i: any) => py.slice(src, i, py.add(i, chunk_size))), () => ([""]));
  return {"chunks": chunks, "order": py.range(py.len(chunks)).map((i: any) => `c${py.format(i, `04d`)}`)};
}
