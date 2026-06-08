/**
 * Converted from Python: core/streaming/chunk_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function chunkText(text: any, chunk_size: any = 4096): any {
  var src: any = py.or2(text, () => (""));
  var chunks: any[] = [];
  var order: any[] = [];
  var step: any = py.max([1, chunk_size]);
  var i: any;
  for (i of py.range(0, py.len(src), step)) {
    var cid: any = `c${py.format(py.floordiv(i, step), `06d`)}`;
    py.listAppend(chunks, {"id": cid, "text": py.slice(src, i, py.add(i, step))});
    py.listAppend(order, cid);
  }
  return {"chunks": chunks, "chunk_order": order};
}
