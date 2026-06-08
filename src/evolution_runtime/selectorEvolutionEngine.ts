/**
 * Converted from Python: core/evolution_runtime/selector_evolution_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function evolveSelectorRuntime(selectors: any = null, healed: any = null): any {
  selectors = py.or2(selectors, () => ({}));
  healed = py.or2(healed, () => ({}));
  var evolved: any[] = [];
  var original: any;
  var replacement: any;
  for ([original, replacement] of py.iter(py.sorted(py.items(healed)))) {
    py.listAppend(evolved, {"original": original, "evolved": replacement, "strategy": "healed_promotion", "fallback": `[data-evolved='${py.toStr(replacement)}']`});
  }
  var selector: any;
  for (selector of py.iter(py.sorted(py.keys(selectors)))) {
    if (py.contains(healed, selector)) {
      continue;
    }
    py.listAppend(evolved, {"original": selector, "evolved": py.at(selectors, selector), "strategy": "structural_upgrade", "fallback": py.at(selectors, selector)});
  }
  return {"selectors": evolved, "count": py.len(evolved), "bounded": true};
}
