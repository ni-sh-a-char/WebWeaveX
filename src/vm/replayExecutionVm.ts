import { replaySemanticEvents } from "../runtime/semanticReplayVm.js";

export function executeReplayVm(events: Array<Record<string, unknown>>): Record<string, unknown> {
  return replaySemanticEvents(events);
}
