import { describe, expect, it, vi } from "vitest";
import { mkdtempSync, rmSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import { tmpdir } from "node:os";
import { RuntimeGraphContract } from "../../src/contracts/graphContracts.js";
import { buildDistributedRuntimeGraph } from "../../src/distributed/distributedRuntimeGraphEngine.js";
import { buildSemanticLineage } from "../../src/semantic/semanticLineage.js";
import { replaySemanticState } from "../../src/semantic/semanticReplay.js";
import { reconstructBrowserState } from "../../src/reconstruction/reconstructBrowser.js";
import { validateFullRuntimeReplay, replayRuntimeState } from "../../src/replay/replayRuntime.js";
import { extractRepositoryDependencies } from "../../src/repository/repositoryDependency.js";
import { normalizeStreamEvents, makeStreamEvent } from "../../src/streaming/streamCapture.js";
import { loadStreamRuntime, saveStreamRuntime } from "../../src/streaming/streamPersistence.js";
import { orchestrateParserFleet } from "../../src/parsers/parserOrchestration.js";
import { buildRuntimeMemoryGraph } from "../../src/memory/runtimeMemoryGraph.js";
import { verifyMemoryLineage, buildMemoryLineage } from "../../src/memory/memoryLineage.js";
import { scheduleExtractionRuntime } from "../../src/distributed/extractionSchedulerEngine.js";
import { federateStreamRuntimes } from "../../src/distributed/distributedStreamEngine.js";
import { buildClusterState } from "../../src/distributed/distributedClusterEngine.js";
import { SemanticMemory } from "../../src/semantic/semanticMemory.js";
import { validateReplayEquivalence } from "../../src/replay/replayEquivalence.js";
import { buildSemanticMemory } from "../../src/semantic/semanticMemory.js";
import { reconcileSemanticStates } from "../../src/semantic/semanticReconciliation.js";
import { createSemanticSnapshot, restoreSemanticSnapshot } from "../../src/semantic/semanticSnapshot.js";
import { buildSemanticPatch } from "../../src/semantic/semanticPatch.js";
import { detectRepositoryLanguages } from "../../src/repository/repositoryLanguageDetection.js";
import { ingestRepository } from "../../src/repository/repositoryIngestion.js";
import * as wwx from "../../src/index.js";
import { buildRuntimeGraph as _buildRuntimeGraph } from "../../src/graph/runtimeGraph.js";

describe("deep branch coverage", () => {
  it("graph contract edge key variants", () => {
    const g = RuntimeGraphContract.normalize({
      nodes: [{ name: "only-name" }, { id: "z", type: "t", name: "z" }],
      edges: [
        { from: "a", to: "b", type: "l" },
        { source: "c", target: "d" },
      ],
    });
    expect(g.edges.length).toBe(2);
  });

  it("distributed graph multi-worker and topology nodes", () => {
    const w1 = { worker_id: "w1" };
    const w2 = { worker_id: "w2" };
    const g = buildDistributedRuntimeGraph([w1, w2], {
      nodes: [{ id: "n1" }, { id: "n2" }],
      edges: [],
    });
    const single = buildDistributedRuntimeGraph([{ worker_id: "solo" }], { nodes: [], edges: [] });
    expect((single.edges as unknown[]).length).toBe(0);
    expect((g.edges as unknown[]).length).toBeGreaterThan(0);
    expect(buildClusterState([w1], []).worker_count).toBe(1);
    expect(federateStreamRuntimes([]).stream_count).toBe(0);
    expect(scheduleExtractionRuntime([], 0).bounded).toBe(true);
  });

  it("semantic lineage and replay branches", () => {
    expect(buildSemanticLineage([{ kind: "a" }, { kind: "b", tick: 2 }]).lineage).toHaveLength(2);
    expect(
      replaySemanticState({
        journal: [{ event_id: "1" }],
        semantic: { entities: { entities: [{ label: "x" }] } },
        history: [{ tick: 0 }],
      }).replayed,
    ).toBe(true);
  });

  it("reconstruct browser with routes", () => {
    const state = reconstructBrowserState({
      browser_ir: { routes: { history: [{ path: "/a" }, { path: "/b" }] } },
    } as never);
    expect(state.tabs.length).toBe(2);
  });

  it("full runtime replay with memory", () => {
    const graph = _buildRuntimeGraph({ n: 1 });
    const mem = wwx.buildRuntimeMemory(graph);
    const orig = {
      unified_runtime_graph: graph,
      runtime_memory: mem,
    } as never;
    const replayed = replayRuntimeState(orig);
    expect(validateFullRuntimeReplay(orig, replayed).equivalent).toBe(true);
  });

  it("repository dependency package.json", () => {
    const dir = mkdtempSync(join(tmpdir(), "wwx-dep-"));
    const pkgPath = join(dir, "package.json");
    writeFileSync(pkgPath, JSON.stringify({ dependencies: { lodash: "^4.0.0" } }));
    const deps = extractRepositoryDependencies([{ path: pkgPath }]);
    expect(Object.keys(deps.dependencies as object).length).toBe(1);
    writeFileSync(join(dir, "bad.json"), "{");
    const bad = extractRepositoryDependencies([{ path: join(dir, "bad.json") }]);
    expect((bad.edges as unknown[]).length).toBe(0);
    rmSync(dir, { recursive: true, force: true });
  });

  it("streaming defaults and persistence", () => {
    expect(normalizeStreamEvents([{}])[0]!.id).toBe("stream_0");
    const dir = mkdtempSync(join(tmpdir(), "wwx-st-"));
    const p = join(dir, "s.json");
    saveStreamRuntime(p, { events: [makeStreamEvent(0, "s", "in", "{}", "c")] }, "k");
    expect((loadStreamRuntime(p, "k").events as unknown[]).length).toBe(1);
    expect((loadStreamRuntime(join(dir, "missing.json"), "k").events as unknown[]).length).toBe(0);
    rmSync(dir, { recursive: true, force: true });
  });

  it("parser fleet and memory graph", () => {
    expect(orchestrateParserFleet([{}, { symbols: { functions: ["f"] } }]).count).toBe(2);
    const g = _buildRuntimeGraph({ x: 1 });
    expect(buildRuntimeMemoryGraph(g, [{ tick: 0 }]).bounded).toBe(true);
    const lineage = buildMemoryLineage([{ tick: 0, kind: "a" }, { tick: 1, kind: "b" }]);
    expect(verifyMemoryLineage(lineage.lineage)).toBe(true);
  });

  it("semantic memory eviction", () => {
    const mem = new SemanticMemory(2);
    mem.put("a", 1);
    mem.put("b", 2);
    mem.put("c", 3, { lineage: true });
    expect(mem.get("a")).toBeUndefined();
    expect(mem.snapshot().count).toBe(2);
  });

  it("replay equivalence keeps the three authority checks for rich envelopes", () => {
    const g = _buildRuntimeGraph({ n: 1 });
    const mem = wwx.buildRuntimeMemory(g);
    const a = {
      unified_runtime_graph: g,
      dom_html: "<div id='x'>1</div>",
      runtime_memory: mem,
      browser_ir: { runtime_identity: "same" },
    } as Record<string, unknown>;
    const b = { ...a, dom_html: "<div id='x'>1</div>" };
    const r = validateReplayEquivalence(a, b as never);
    expect(r.equivalent).toBe(true);
    expect(r.checks.map((c) => c.name)).toEqual(["graph_hash", "global_fingerprint", "browser_identity"]);
  });

  it("reconstruct browser default tabs and semantic helpers", () => {
    const emptyRoutes = reconstructBrowserState({ browser_ir: {} } as never);
    expect(emptyRoutes.tabs[0]!.path).toBe("/");
    const withSession = reconstructBrowserState({ browser_ir: {} } as never, wwx.createRuntimeSession({}));
    expect(withSession.session.session_id).toBeTruthy();
    expect(buildSemanticMemory({ semantic: { entities: { entities: [{ type: "login" }] } } }).concepts).toContain(
      "login",
    );
    expect(reconcileSemanticStates([]).count).toBe(0);
    const snap = createSemanticSnapshot({ z: 1 });
    expect(restoreSemanticSnapshot(snap).z).toBe(1);
    expect(buildSemanticPatch({ a: 1 }, { b: 2 }).added).toHaveProperty("b");
  });

  it("repository ingest skip and language detection", () => {
    expect(ingestRepository("Z:\\no-such-path-wwx-999").available).toBe(false);
    expect(
      detectRepositoryLanguages([{ extension: ".ts" }, { extension: "" }, { extension: ".ts" }]).primary,
    ).toBe(".ts");
  });

  it("capture runtime unavailable branch", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn(async () => {
        throw new Error("net");
      }),
    );
    const cap = await wwx.captureRuntime("https://offline.invalid");
    expect(cap.available).toBe(false);
    vi.unstubAllGlobals();
  });
});
