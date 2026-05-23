export type UniversalInput = {
  source: string;
  sourceType?: "auto" | "web" | "document" | "repository" | "multimodal" | "text";
  url?: string;
  path?: string;
  session?: Record<string, unknown>;
};

export type PipelineOptions = {
  authenticated?: boolean;
  sessionPath?: string;
  encryptionKey?: string;
  semanticRuntime?: boolean;
  federatedMemory?: boolean;
  reconstructionRuntime?: boolean;
};

export type ExtractionEnvelope = {
  bounded?: boolean;
  unified_runtime_graph?: RuntimeGraphRef;
  browser_ir?: Record<string, unknown>;
  runtime?: Record<string, unknown>;
  pipeline_hash?: string;
  global_runtime_fingerprint?: string;
  [key: string]: unknown;
};

import type { RuntimeGraph } from "./graphContracts.js";

export type RuntimeGraphRef = RuntimeGraph;
