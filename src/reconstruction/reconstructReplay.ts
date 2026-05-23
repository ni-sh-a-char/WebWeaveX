import type { ExtractionEnvelope } from "../contracts/runtimeContracts.js";
import { replayRuntimeState, validateFullRuntimeReplay } from "../replay/replayRuntime.js";
import { reconstructRuntimeGraph } from "./reconstructGraph.js";
import { reconstructMemoryFromEnvelope } from "./reconstructMemory.js";
import { reconstructBrowserState } from "./reconstructBrowser.js";

export function reconstructReplayState(extraction: ExtractionEnvelope): {
  replayed: ExtractionEnvelope;
  graph: ReturnType<typeof reconstructRuntimeGraph>;
  memory: Record<string, unknown>;
  browser: ReturnType<typeof reconstructBrowserState>;
  validation: ReturnType<typeof validateFullRuntimeReplay>;
  bounded: boolean;
} {
  const replayed = replayRuntimeState(extraction);
  const graph = reconstructRuntimeGraph(extraction);
  const memory = reconstructMemoryFromEnvelope(extraction as Record<string, unknown>);
  const browser = reconstructBrowserState(extraction);
  const validation = validateFullRuntimeReplay(extraction, replayed);
  return { replayed, graph, memory, browser, validation, bounded: true };
}
