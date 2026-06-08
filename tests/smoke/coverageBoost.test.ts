import { describe, expect, it } from "vitest";
import * as wwx from "../../src/index.js";
import { buildRuntimeGraph as _buildRuntimeGraph } from "../../src/graph/runtimeGraph.js";
import { ingestRepository } from "../../src/repository/repositoryIngestion.js";
import { mergeSemanticStates } from "../../src/semantic/semanticMerge.js";
import { healSelector, computeDomSimilarity } from "../../src/adaptive/selectorHealing.js";
import { graphReplayHash, validateGraphReplayEquivalence } from "../../src/replay/replayGraph.js";
import { memoryReplayHash, validateMemoryReplayEquivalence } from "../../src/replay/replayMemory.js";
import { replayRuntimeState } from "../../src/replay/replayRuntime.js";
import { identityFromExtraction, compareBrowserIdentity } from "../../src/browser/browserIdentity.js";
import { rotateRuntimeSession } from "../../src/browser/runtimeSession.js";
import { queryRuntimeGraph } from "../../src/graph/runtimeGraph.js";
import { validateRuntimeGraph } from "../../src/graph/runtimeGraph.js";
import { buildRuntimeGraphLineage } from "../../src/graph/runtimeGraphLineage.js";
import { buildDistributedRuntimeGraph } from "../../src/distributed/distributedRuntimeGraphEngine.js";
import { replayStreamEvents } from "../../src/streaming/streamReplay.js";
import { replaySemanticState } from "../../src/semantic/semanticReplay.js";
import { reconstructBrowserState } from "../../src/reconstruction/reconstructBrowser.js";

describe("coverage boost", () => {
  it("repository unavailable path", () => {
    const r = ingestRepository("Z:\\nonexistent-webweavex-path-99999");
    expect(r.available).toBe(false);
  });

  it("semantic merge conflict branch", () => {
    const m = mergeSemanticStates({ a: 1 }, { a: 2 });
    expect((m.state as Record<string, unknown>).a).toMatchObject({ conflict: true });
  });

  it("adaptive selector strategies", () => {
    const h = healSelector("#login", [
      { tag: "button", text: "login", attrs: { "data-testid": "login-btn" } },
    ]);
    expect((h.strategies as unknown[]).length).toBeGreaterThan(0);
    expect(computeDomSimilarity("a b", "a c")).toBeGreaterThan(0);
  });

  it("graph and memory replay exports", () => {
    const g = _buildRuntimeGraph({ n: 1 });
    const rg = wwx.replayRuntimeGraph(g);
    expect(validateGraphReplayEquivalence(g, rg).equivalent).toBe(true);
    expect(graphReplayHash(g)).toBeTruthy();
    const mem = wwx.buildRuntimeMemory(g);
    const rm = wwx.replayRuntimeMemory(g, []);
    expect(validateMemoryReplayEquivalence(mem, rm).equivalent).toBe(true);
    expect(memoryReplayHash(g, [])).toBeTruthy();
    expect(queryRuntimeGraph(g).nodes.length).toBeGreaterThan(0);
    expect(validateRuntimeGraph(g).valid).toBe(true);
  });

  it("lineage streaming semantic browser reconstruct", () => {
    const g1 = _buildRuntimeGraph({ a: 1 });
    const g2 = _buildRuntimeGraph({ b: 2 });
    expect(buildRuntimeGraphLineage([g1, g2]).graph_count).toBe(2);
    const worker = { worker_id: "w1", status: "idle" };
    const distGraph = buildDistributedRuntimeGraph([worker], {
      nodes: [{ id: "n1", type: "runtime" }],
      edges: [{ from: "n1", to: "n1" }],
    });
    expect((distGraph.nodes as unknown[]).length).toBeGreaterThan(1);
    expect(replayStreamEvents([]).replayed).toEqual([]);
    expect(replaySemanticState({ journal: [{ e: 1 }], semantic: {} }).replayed).toBe(true);
    expect(
      reconstructBrowserState({ browser_ir: { url: "https://x.test" } }).bounded,
    ).toBe(true);
  });

  it("replay runtime and browser identity", () => {
    const g = _buildRuntimeGraph({ u: 1 });
    const envelope = { unified_runtime_graph: g, extraction: { url: "https://x.test" } };
    const replayed = replayRuntimeState(envelope);
    expect(wwx.validateFullRuntimeReplay(envelope, replayed).equivalent).toBe(true);
    const id = identityFromExtraction({
      browser_ir: { url: "https://x.test", dom_hash: "h" },
      unified_runtime_graph: g,
    } as never);
    const id2 = { ...id, runtime_identity: id.runtime_identity };
    expect(compareBrowserIdentity(id, id2).equivalent).toBe(true);
    const session = wwx.createRuntimeSession({ cookies: [{ name: "c", value: "v" }] });
    expect(rotateRuntimeSession(session).session_id).toBeTruthy();
  });
});
