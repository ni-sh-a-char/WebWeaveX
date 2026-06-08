/**
 * Converted from Python: core/execution/runtime_simulation_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { executeRuntimeAction } from "./runtimeExecutionEngine.js";
import { trackRuntimeMutations } from "./runtimeMutationEngine.js";
import { buildRuntimeSandbox } from "./runtimeSandboxEngine.js";

export function simulateRuntimeExecution(actions: any, sandbox: any = null, tick: any = 0): any {
  sandbox = py.or2(sandbox, () => (buildRuntimeSandbox()));
  var predicted: any[] = [];
  var rollback_required: any = false;
  var index: any;
  var raw: any;
  for ([index, raw] of py.enumerate(py.slice(actions, null, 1000))) {
    var result: any = executeRuntimeAction(raw, sandbox, undefined, undefined, py.add(tick, index));
    if (py.truthy(py.get(result, "executed"))) {
      py.listAppend(predicted, {"kind": py.toStr(py.get(raw, "type", "action")), "target": py.toStr(py.get(raw, "selector", py.get(raw, "window", py.get(raw, "command", "")))), "tick": py.add(tick, index)});
    } else {
      rollback_required = true;
    }
  }
  var mutation_view: any = trackRuntimeMutations(undefined, {"kind": "simulated", "target": "dry_run", "tick": tick});
  return {"simulated": true, "predicted_mutations": predicted, "rollback_required": rollback_required, "mutation_preview": py.get(mutation_view, "mutations", []), "runtime_mutated": false, "bounded": true};
}
export { buildRuntimeSandbox, executeRuntimeAction, trackRuntimeMutations };
