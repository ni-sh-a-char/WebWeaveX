/**
 * Converted from Python: core/runtime/runtime_state_machine_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "./pyCompat.js";

export let VALID_TRANSITIONS: any = {"initialized": new Set(["scheduled", "failed"]), "scheduled": new Set(["running", "failed"]), "running": new Set(["completed", "failed", "retrying"]), "retrying": new Set(["running", "failed"]), "completed": new Set(), "failed": new Set()};
export class RuntimeTransition {
  declare previous: any;
  declare current: any;
  declare valid: any;
  declare evidence: any;
  constructor(previous: any, current: any, valid: any, evidence: any) {
    this.previous = previous;
    this.current = current;
    this.valid = valid;
    this.evidence = evidence;
  }
}
export class RuntimeStateMachine {
  declare _history: any;
  declare _state: any;
  constructor() {
    this._history = [];
    this._state = "initialized";
  }
  get state(): any {
    return this._state;
  }
  get history(): any {
    return [...py.iter(this._history)];
  }
  transition(next_state: any, evidence: any = null): any {
    evidence = py.sorted(py.toSet(py.or2(evidence, () => ([]))));
    var valid: any = py.contains(py.get(VALID_TRANSITIONS, this._state, new Set()), next_state);
    var transition: any = new RuntimeTransition(this._state, next_state, valid, evidence);
    py.listAppend(this._history, transition);
    if (py.truthy(valid)) {
      this._state = next_state;
    }
    return transition;
  }
}
