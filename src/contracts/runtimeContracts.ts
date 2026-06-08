/**
 * Converted from Python: core/contracts/runtime_contracts.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export class RuntimePhase {
  static INGESTION = "ingestion";
  static EXECUTION = "execution";
  static SEMANTIC = "semantic";
  static CAUSALITY = "causality";
  static SYNCHRONIZATION = "synchronization";
  static MEMORY = "memory";
  static RECONSTRUCTION = "reconstruction";
  static GRAPH = "graph";
}
(RuntimePhase.prototype as Record<string, any>)["INGESTION"] = (RuntimePhase as Record<string, any>)["INGESTION"];
(RuntimePhase.prototype as Record<string, any>)["EXECUTION"] = (RuntimePhase as Record<string, any>)["EXECUTION"];
(RuntimePhase.prototype as Record<string, any>)["SEMANTIC"] = (RuntimePhase as Record<string, any>)["SEMANTIC"];
(RuntimePhase.prototype as Record<string, any>)["CAUSALITY"] = (RuntimePhase as Record<string, any>)["CAUSALITY"];
(RuntimePhase.prototype as Record<string, any>)["SYNCHRONIZATION"] = (RuntimePhase as Record<string, any>)["SYNCHRONIZATION"];
(RuntimePhase.prototype as Record<string, any>)["MEMORY"] = (RuntimePhase as Record<string, any>)["MEMORY"];
(RuntimePhase.prototype as Record<string, any>)["RECONSTRUCTION"] = (RuntimePhase as Record<string, any>)["RECONSTRUCTION"];
(RuntimePhase.prototype as Record<string, any>)["GRAPH"] = (RuntimePhase as Record<string, any>)["GRAPH"];
export class UniversalInput {
  constructor(source: any, source_type: any = "auto", url: any = "", path: any = "", session: any = null, options: any = {}, tick: any = 0) {
    this.source = source;
    this.source_type = source_type;
    this.url = url;
    this.path = path;
    this.session = session;
    this.options = options;
    this.tick = tick;
  }
  to_dict(): any {
    return {"source": this.source, "source_type": this.source_type, "url": this.url, "path": this.path, "session": py.or2(this.session, () => ({})), "options": py.pyDict(py.sorted(py.items(this.options))), "tick": this.tick, "bounded": true};
  }
}

/* ------------------------------------------------------------------ */
/* TypeScript-only contract types (runtime-invisible; hand-maintained) */
/* ------------------------------------------------------------------ */

import type { RuntimeGraph } from "./graphContracts.js";

export type RuntimeGraphRef = RuntimeGraph;

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

/* declaration merge: dataclass fields + legacy camel alias for the pipeline.
 * Only `source` is required — every other dataclass field has a default,
 * so plain-object callers may omit them (mirrors Python's dict inputs). */
export interface UniversalInput {
  source: string;
  source_type?: string;
  url?: string;
  path?: string;
  session?: Record<string, unknown> | null;
  options?: Record<string, unknown>;
  tick?: number;
  sourceType?: string;
}

/* structural input shape: the pipeline accepts plain objects (Python takes
 * dicts as well as UniversalInput instances) — no to_dict required */
export type UniversalInputLike = Omit<UniversalInput, "to_dict">;
