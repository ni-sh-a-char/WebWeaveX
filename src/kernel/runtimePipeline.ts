import { extractWeb } from "../browser/extractWeb.js";
import { buildRuntimeGraph } from "../graph/runtimeGraph.js";
import { computeKaalkaHashPayload } from "../crypto/kaalkaHash.js";
import { computeGlobalRuntimeFingerprint } from "../determinism/globalRuntimeFingerprint.js";
import type { UniversalInput, PipelineOptions, ExtractionEnvelope } from "../contracts/runtimeContracts.js";

function detectKind(inp: UniversalInput): string {
  if (inp.sourceType && inp.sourceType !== "auto") return inp.sourceType;
  const src = inp.url ?? inp.path ?? inp.source;
  if (src.startsWith("http://") || src.startsWith("https://")) return "web";
  if (/\.(pdf|docx|md|html|txt)$/i.test(src)) return "document";
  return "text";
}

export async function runCanonicalPipeline(
  inp: UniversalInput,
  options: PipelineOptions = {},
): Promise<ExtractionEnvelope & { ingestion: Record<string, unknown> }> {
  const kind = detectKind(inp);
  const target = inp.url ?? inp.path ?? inp.source;

  let extraction: ExtractionEnvelope;
  if (kind === "web") {
    extraction = await extractWeb(target, {
      authenticated: options.authenticated,
      sessionPath: options.sessionPath,
      encryptionKey: options.encryptionKey,
      semanticRuntime: options.semanticRuntime,
    });
  } else {
    const graph = buildRuntimeGraph({ text: { source: target } });
    extraction = {
      bounded: true,
      unified_runtime_graph: graph,
      runtime: { available: false, kind },
      pipeline_hash: computeKaalkaHashPayload({ target, kind }),
    };
    extraction.global_runtime_fingerprint = computeGlobalRuntimeFingerprint(extraction, graph);
  }

  return {
    ...extraction,
    ingestion: {
      path: target,
      type: kind,
      supported: true,
      bounded: true,
    },
  };
}
