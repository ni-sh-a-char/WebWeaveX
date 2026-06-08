/**
 * Converted from Python: core/kernel/runtime_dispatcher.py
 * @generated — WebWeaveX python→javascript library port
 */


export function dispatchRuntimePhase(phase: any, handler: any, context: any, kwargs: Record<string, any> = {}): any {
  var result: any = handler(context, ...Object.values(kwargs));
  return {"phase": phase, "result": result, "dispatched": true, "bounded": true};
}
