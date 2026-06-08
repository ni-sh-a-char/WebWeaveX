/**
 * Converted from Python: core/evolution_runtime/runtime_repair_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function repairRuntimeFailures(failures: any = null, selectors: any = null): any {
  failures = py.or2(failures, () => ([]));
  selectors = py.or2(selectors, () => ({}));
  var repairs: any[] = [];
  var repair_map: any = {"broken_selector": "heal_selector", "failed_workflow": "reorder_workflow", "sync_divergence": "resync_runtime", "runtime_inconsistency": "verify_consistency", "causality_gap": "bridge_causality"};
  var failure: any;
  for (failure of py.iter(py.sorted(failures))) {
    var action: any = py.get(repair_map, failure, "retry_step");
    py.listAppend(repairs, {"failure": failure, "action": action, "repaired": true});
  }
  var selector: any;
  var healed: any;
  for ([selector, healed] of py.iter(py.sorted(py.items(selectors)))) {
    py.listAppend(repairs, {"failure": "broken_selector", "action": "heal_selector", "selector": selector, "healed": healed, "repaired": true});
  }
  return {"repairs": repairs, "repair_count": py.len(repairs), "bounded": true};
}
