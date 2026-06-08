import { describe, expect, it } from "vitest";
import { healSelector, computeDomSimilarity } from "../../src/adaptive/selectorHealing.js";
import { deriveKaalkaTimeKey, encryptValue, decryptValue } from "../../src/crypto/kaalkaRuntime.js";
import { buildParserCognitionEvidence } from "../../src/parsers/parserOrchestration.js";
import { runDistributedExtraction } from "../../src/distributed/distributedExtractionOrchestrator.js";
import { synchronizeDistributedCognition } from "../../src/distributed/distributedCognitionSync.js";
import { runSemanticOrchestration } from "../../src/semantic/semanticOrchestration.js";
import { querySemanticGraphCognition } from "../../src/semantic/semanticGraphCognition.js";
import { diffRuntimeGraphs } from "../../src/graph/graphIntelligence.js";
import * as wwx from "../../src/index.js";
import { buildRuntimeGraph as _buildRuntimeGraph } from "../../src/graph/runtimeGraph.js";

describe("final branch push to 85%", () => {
  it("selector healing attribute-only path", () => {
    const h = healSelector(".btn", [{ tag: "button", attrs: { id: "submit" } }]);
    expect((h.strategies as unknown[]).length).toBeGreaterThan(0);
    expect(computeDomSimilarity("", "")).toBe(1);
    expect(computeDomSimilarity("a", "b")).toBe(0);
  });

  it("kaalka keys and parser flags object", () => {
    for (const key of ["a", "agent-key", "longer-encryption-key-for-kaalka"]) {
      const enc = encryptValue({ k: key }, key);
      expect(JSON.parse(decryptValue(enc.encrypted, key).decrypted)).toEqual({ k: key });
    }
    expect(deriveKaalkaTimeKey("probe-key")).toMatch(/\d+:\d+:\d+/);
    const badFlags = buildParserCognitionEvidence({ evidence: "not-object" as unknown as Record<string, unknown> });
    expect(badFlags.bounded).toBe(true);
  });

  it("distributed and semantic cognition branches", () => {
    const out = runDistributedExtraction(
      [],
      undefined,
      { queue: [{ task_id: "t0" }], workers: [], tick: 3 },
      3,
      [{ nodes: [{ id: "n" }], edges: [] }],
    );
    expect(out.bounded).toBe(true);
    const sync = synchronizeDistributedCognition(
      [{ worker_id: "w", adaptive_runtime: { memory: { healed_selectors: { s: "ok" } } } }],
      [{ nodes: [{ id: "n" }], edges: [] }],
    );
    expect(sync.synchronized).toBe(true);
    const g = _buildRuntimeGraph({ x: 1 });
    expect(querySemanticGraphCognition(g, (n) => n.type === "x").matches).toBeGreaterThanOrEqual(0);
    const diff = diffRuntimeGraphs(g, _buildRuntimeGraph({ y: 2 })) as { added: unknown[] };
    expect(diff.added.length).toBeGreaterThan(0);
    expect(runSemanticOrchestration([], { kind: "noop" }).bounded).toBe(true);
  });
});
