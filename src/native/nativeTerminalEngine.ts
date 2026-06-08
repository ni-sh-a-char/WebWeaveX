/**
 * Converted from Python: core/native/native_terminal_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function captureTerminalRuntime(lines: any = null, snapshot: any = null): any {
  var snap: any = py.or2(snapshot, () => ({}));
  var output: any = py.slice([...py.iter(py.or2(lines, () => (py.get(snap, "output", []))))], null, 50000);
  var commands: any = py.slice([...py.iter(py.get(snap, "commands", []))], null, 10000);
  var prompts: any = py.slice([...py.iter(py.get(snap, "prompts", []))], null, 1000);
  var ansi_state: any = _parseAnsiState(output);
  var stream_id: any = py.toStr(py.get(snap, "stream_id", "terminal:0"));
  return {"stream_id": stream_id, "output": output, "commands": commands, "prompts": prompts, "ansi_state": ansi_state, "replay_token": _terminalReplayToken(output, commands), "bounded": true};
}
export function _parseAnsiState(lines: any): any {
  var bold: any = false;
  var color: any = "default";
  var line: any;
  for (line of py.iter(py.slice(lines, null, 5000))) {
    if (py.contains(line, "\u001b[1m")) {
      bold = true;
    }
    if (py.contains(line, "\u001b[32m")) {
      color = "green";
    } else if (py.contains(line, "\u001b[31m")) {
      color = "red";
    }
  }
  return {"bold": bold, "color": color, "bounded": true};
}
export function _terminalReplayToken(output: any, commands: any): any {
  var parts: any = py.add(py.add(py.join("|", py.slice(commands, null, 100)), "::"), py.join("\n", py.slice(output, null, 500)));
  return py.slice(py.hashNew("sha256", py.encode(parts, "utf-8")).hexdigest(), null, 32);
}
