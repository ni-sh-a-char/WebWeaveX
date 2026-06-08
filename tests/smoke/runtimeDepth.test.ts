import { describe, expect, it } from "vitest";
import { mkdtempSync, rmSync } from "node:fs";
import { join } from "node:path";
import { tmpdir } from "node:os";
import * as wwx from "../../src/index.js";
import { buildRuntimeGraph as _buildRuntimeGraph } from "../../src/graph/runtimeGraph.js";
import { SemanticMemory } from "../../src/semantic/semanticMemory.js";
import { orchestrate } from "../../src/orchestration/orchestrationEngine.js";
import { replayDomSnapshot } from "../../src/replay/replayDom.js";
import {
  computeReplayFingerprint,
  validateFingerprintReplayEquivalence,
} from "../../src/replay/replayFingerprint.js";
import { validateMemoryReplay } from "../../src/memory/memoryReplay.js";
import { saveRuntimeMemory, loadRuntimeMemory } from "../../src/memory/memoryPersistence.js";
import { verifyMemoryLineage } from "../../src/memory/memoryLineage.js";
import { mergeGraphReplay } from "../../src/graph/runtimeGraphReplay.js";
import { rebuildGraphFromPartial } from "../../src/graph/runtimeGraphReconstruction.js";

describe("runtime depth smoke", () => {
  it("memory persistence and lineage", () => {
    const graph = _buildRuntimeGraph({ s: 1 });
    const dir = mkdtempSync(join(tmpdir(), "wwx-mem-"));
    const path = join(dir, "mem.json");
    saveRuntimeMemory(path, wwx.buildRuntimeMemory(graph), "key");
    const loaded = loadRuntimeMemory(path, "key");
    expect(loaded.bounded).toBe(true);
    const lineage = wwx.buildMemoryLineage([{ tick: 1, kind: "step" }]);
    expect(verifyMemoryLineage(lineage.lineage)).toBe(true);
    const mem = wwx.buildRuntimeMemory(graph, []);
    expect(validateMemoryReplay(mem, wwx.replayMemoryState(graph, []))).toBe(true);
    rmSync(dir, { recursive: true, force: true });
  });

  it("semantic and orchestration", () => {
    const mem = new SemanticMemory();
    mem.put("k", { v: 1 });
    expect(mem.get("k")).toEqual({ v: 1 });
    const built = wwx.buildSemanticMemory({ entities: { entities: [{ label: "x" }] } });
    expect(built.bounded).toBe(true);
    const orch = orchestrate("https://example.com/extract");
    expect(orch.plan).toBeDefined();
    expect(orch.strategy).toBeDefined();
    expect(wwx.runSemanticRuntime({}, { kind: "event", payload: { a: 1 } }).bounded).toBe(true);
  });

  it("replay fingerprint and dom", () => {
    const html = "<div>ok</div>";
    expect(replayDomSnapshot(html).hash).toBeTruthy();
    expect(wwx.validateDomReplayEquivalence(html, html)).toBe(true);
    const g = _buildRuntimeGraph({ dom: html });
    const envelope = { unified_runtime_graph: g, graph: g };
    expect(computeReplayFingerprint(envelope, g).length).toBeGreaterThan(0);
    expect(validateFingerprintReplayEquivalence(envelope, envelope, g).equivalent).toBe(true);
  });

  it("graph merge and partial rebuild", () => {
    const g1 = _buildRuntimeGraph({ a: 1 });
    const g2 = _buildRuntimeGraph({ b: 2 });
    const merged = mergeGraphReplay(g1, g2);
    expect(merged.nodes.length).toBeGreaterThan(0);
    const partial = rebuildGraphFromPartial({ nodes: [{ id: "x" }], edges: [], bounded: true });
    expect(partial.bounded).toBe(true);
  });

  it("runtime session and snapshots", async () => {
    const session = wwx.createRuntimeSession({ cookies: [] });
    expect(session.session_id).toBeTruthy();
    const dir = mkdtempSync(join(tmpdir(), "wwx-sess-"));
    const path = join(dir, "session.kaalka");
    wwx.persistRuntimeSession(path, session, "session-key");
    const restored = wwx.restoreRuntimeSession(path, "session-key");
    rmSync(dir, { recursive: true, force: true });
    expect(restored.session_id).toBe(session.session_id);
    const snap = await wwx.captureRuntimeSnapshot("https://example.com", 0, session);
    expect(wwx.compareRuntimeSnapshots(snap, snap).equivalent).toBe(true);
  });

  it("memory merge replicate query", () => {
    const g = _buildRuntimeGraph({ q: 1 });
    const m1 = wwx.buildRuntimeMemory(g, [{ tick: 0 }]);
    const m2 = wwx.buildRuntimeMemory(g, [{ tick: 1 }]);
    const merged = wwx.mergeRuntimeMemories(m1, m2);
    expect((merged.memory as Record<string, unknown>).runtime_history).toBeDefined();
    expect(wwx.replicateRuntimeMemory(m1).stable_hash).toBe(m1.stable_hash);
    expect(wwx.queryRuntimeMemory(m1, "graph")).toBeDefined();
  });
});
