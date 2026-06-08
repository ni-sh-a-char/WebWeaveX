/**
 * Converted from Python: core/universal/protobuf_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function parseProtobuf(text: any): any {
  var src: any = py.or2(text, () => (""));
  var messages: any = py.sorted(py.toSet(py.reFindall("\\bmessage\\s+([A-Za-z_][A-Za-z0-9_]*)\\b", src, "")));
  var services: any = py.sorted(py.toSet(py.reFindall("\\bservice\\s+([A-Za-z_][A-Za-z0-9_]*)\\b", src, "")));
  return {"messages": messages, "services": services};
}
