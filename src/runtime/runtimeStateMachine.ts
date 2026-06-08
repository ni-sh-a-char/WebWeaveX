const TRANSITIONS: Record<string, string[]> = {
  initialized: ["running", "failed"],
  running: ["paused", "failed", "completed"],
  paused: ["running", "failed"],
  failed: ["running"],
  completed: [],
};

export function transitionRuntimeState(current: string, next: string): Record<string, unknown> {
  const allowed = TRANSITIONS[current] ?? [];
  const valid = allowed.includes(next);
  return {
    valid,
    from: current,
    to: valid ? next : current,
    bounded: true,
  };
}

export class RuntimeStateMachine {
  state = "initialized";

  transition(next: string): string {
    const result = transitionRuntimeState(this.state, next);
    if (result.valid) this.state = next;
    return this.state;
  }
}
