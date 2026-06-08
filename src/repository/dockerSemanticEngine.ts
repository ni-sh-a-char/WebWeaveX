/**
 * Converted from Python: core/repository/docker_semantic_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function parseDockerfileSemantics(text: any): any {
  var instructions: any[] = [];
  var line: any;
  for (line of py.iter(py.splitlines(text))) {
    line = py.strip(line);
    if (!py.truthy(line)) {
      continue;
    }
    if (py.truthy(py.startswith(line, "#"))) {
      continue;
    }
    var op: any = String(py.at(py.split(line), 0)).toUpperCase();
    py.listAppend(instructions, {"instruction": op, "raw": line});
  }
  return {"instructions": instructions, "count": py.len(instructions), "grounded": true};
}
