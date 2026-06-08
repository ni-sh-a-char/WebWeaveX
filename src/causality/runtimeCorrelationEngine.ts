/**
 * Converted from Python: core/causality/runtime_correlation_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function correlateRuntimeMutations(browser_events: any = null, native_events: any = null, notifications: any = null, terminal_lines: any = null, process_events: any = null): any {
  var correlations: any[] = [];
  var step: any = 0;
  var event: any;
  for (event of py.iter([...py.iter(py.or2(browser_events, () => ([])))])) {
    py.listAppend(correlations, {"kind": "ui_change", "event_id": py.toStr(py.get(event, "id", `browser:${py.toStr(step)}`)), "runtime": "browser", "step": step});
    step = py.add(step, 1);
  }
  var line: any;
  for (line of py.iter(py.slice([...py.iter(py.or2(terminal_lines, () => ([])))], null, 1000))) {
    py.listAppend(correlations, {"kind": "terminal_log", "line": line, "runtime": "terminal", "step": step});
    step = py.add(step, 1);
  }
  var notification: any;
  for (notification of py.iter([...py.iter(py.or2(notifications, () => ([])))])) {
    py.listAppend(correlations, {"kind": "notification", "payload": notification, "runtime": "desktop", "step": step});
    step = py.add(step, 1);
  }
  for (event of py.iter([...py.iter(py.or2(native_events, () => ([])))])) {
    py.listAppend(correlations, {"kind": "native_mutation", "event_id": py.toStr(py.get(event, "id", "")), "runtime": py.toStr(py.get(event, "runtime", "desktop")), "step": step});
    step = py.add(step, 1);
  }
  var proc: any;
  for (proc of py.iter([...py.iter(py.or2(process_events, () => ([])))])) {
    py.listAppend(correlations, {"kind": "process_mutation", "process": py.toStr(py.get(proc, "name", "")), "runtime": "process", "step": step});
    step = py.add(step, 1);
  }
  return {"correlations": py.sorted(correlations, {key: ((item: any) => py.at(item, "step")) as (item: any) => any}), "count": py.len(correlations), "bounded": true};
}
