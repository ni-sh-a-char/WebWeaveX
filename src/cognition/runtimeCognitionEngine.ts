import { buildRuntimeGraph } from "../graph/runtimeGraph.js";
import { computeDeterministicHash } from "../crypto/kaalkaRuntime.js";
import { recoverRuntime } from "../runtime/runtimeRecoveryEngine.js";

export function runRuntimeCognitionTick(
  session: Record<string, unknown> = {},
  signals: Record<string, unknown>[] = [],
  events: Array<Record<string, unknown>> = [],
): Record<string, unknown> {
  const graph = buildRuntimeGraph({ cognition: { session, signal_count: signals.length } });
  const recovery = recoverRuntime("initialized", events.map((e) => String(e.id ?? "e")));
  return {
    bounded: true,
    cognition_id: computeDeterministicHash({ session, signals, events }),
    graph,
    recovery,
    event_count: events.length,
  };
}
