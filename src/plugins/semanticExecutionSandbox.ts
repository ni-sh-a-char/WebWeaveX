/**
 * Converted from Python: core/plugins/semantic_execution_sandbox.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_SANDBOX_KEYS: any = 1000;
export class SemanticExecutionSandbox {
  declare _state: any;
  constructor() {
    this._state = {};
  }
  put(key: any, value: any): any {
    if ((py.truthy(py.startswith(key, "__")) || (py.len(this._state) >= MAX_SANDBOX_KEYS))) {
      return false;
    }
    py.setItem(this._state, key, value);
    return true;
  }
  get(key: any): any {
    return py.get(this._state, key);
  }
  snapshot(): any {
    return py.pyDict(py.sorted(py.items(this._state)));
  }
}
