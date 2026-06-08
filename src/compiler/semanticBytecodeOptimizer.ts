/**
 * Converted from Python: core/compiler/semantic_bytecode_optimizer.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function optimizeSemanticBytecode(instructions: any): any {
  var optimized: any[] = [];
  var seen: Set<any> = new Set();
  var instruction: any;
  for (instruction of py.iter(instructions)) {
    var fingerprint: any = py.toStr(instruction);
    if (py.contains(seen, fingerprint)) {
      continue;
    }
    py.setAdd(seen, fingerprint);
    py.listAppend(optimized, instruction);
  }
  return {"instructions": optimized, "optimized": true};
}
