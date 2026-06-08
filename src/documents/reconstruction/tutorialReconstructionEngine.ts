/**
 * Converted from Python: core/documents/reconstruction/tutorial_reconstruction_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";

export function reconstructTutorial(text: any): any {
  var steps: any = py.sorted(py.toSet(py.reFindall("^\\s*\\d+\\.\\s+(.+)$", py.or2(text, () => ("")), "m")));
  var flow: any = py.range(py.max([0, py.sub(py.len(steps), 1)])).map((i: any) => ({"from": py.at(steps, i), "to": py.at(steps, py.add(i, 1))}));
  return {"steps": steps, "flow": flow};
}
