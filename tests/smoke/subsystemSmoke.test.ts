import { describe, expect, it, vi } from "vitest";
import { mkdtempSync, rmSync } from "node:fs";
import { join } from "node:path";
import { tmpdir } from "node:os";
import * as wwx from "../../src/index.js";
import { buildRuntimeGraph as _buildRuntimeGraph } from "../../src/graph/runtimeGraph.js";
import { extractApiRuntime } from "../../src/connectors/apiConnector.js";
import { extractCicdRuntime } from "../../src/connectors/cicdConnector.js";
import { extractContainerRuntime } from "../../src/connectors/containerConnector.js";
import { extractDatabaseRuntime } from "../../src/connectors/databaseConnector.js";
import { extractDockerRuntime } from "../../src/connectors/dockerConnector.js";
import { extractFilesystemRuntime } from "../../src/connectors/filesystemConnector.js";
import { extractGraphqlRuntime } from "../../src/connectors/graphqlConnector.js";
import { extractGrpcRuntime } from "../../src/connectors/grpcConnector.js";
import { extractIdeRuntime } from "../../src/connectors/ideConnector.js";
import { extractKafkaRuntime } from "../../src/connectors/kafkaConnector.js";
import { extractKubernetesRuntime } from "../../src/connectors/kubernetesConnector.js";
import {
  runLiveForExtraction,
  runLiveRuntime,
} from "../../src/connectors/liveRuntimeOrchestrator.js";
import {
  loadLiveRuntimeMemory,
  saveLiveRuntimeMemory,
} from "../../src/connectors/liveRuntimeMemory.js";
import { extractMysqlRuntime } from "../../src/connectors/mysqlConnector.js";
import { extractPostgresRuntime } from "../../src/connectors/postgresConnector.js";
import { extractRedisRuntime } from "../../src/connectors/redisConnector.js";
import { extractRuntimeStreamRuntime } from "../../src/connectors/runtimeStreamConnector.js";
import { extractSqliteRuntime } from "../../src/connectors/sqliteConnector.js";
import { extractTelemetryRuntime } from "../../src/connectors/telemetryConnector.js";
import { extractWebsocketRuntime } from "../../src/connectors/websocketConnector.js";
import { buildClusterState } from "../../src/distributed/distributedClusterEngine.js";
import { synchronizeAdaptiveRuntime } from "../../src/distributed/distributedAdaptiveRuntimeEngine.js";
import { routeBrowserIdentity } from "../../src/distributed/distributedIdentityEngine.js";
import { monitorExtractionCluster } from "../../src/distributed/distributedMonitoringEngine.js";
import { recoverDistributedRuntime } from "../../src/distributed/distributedRecoveryEngine.js";
import { buildDistributedRuntimeGraph } from "../../src/distributed/distributedRuntimeGraphEngine.js";
import { routeAuthenticatedSessions } from "../../src/distributed/distributedSessionEngine.js";
import { federateStreamRuntimes } from "../../src/distributed/distributedStreamEngine.js";
import { balanceExtractionWorkloads } from "../../src/distributed/distributedLoadBalancer.js";
import { dequeueExtraction, enqueueExtraction } from "../../src/distributed/extractionQueueEngine.js";
import { scheduleExtractionRuntime } from "../../src/distributed/extractionSchedulerEngine.js";
import { createExtractionWorker } from "../../src/distributed/extractionWorkerEngine.js";
import { federateExtractionRuntimes } from "../../src/distributed/runtimeFederationEngine.js";
import { buildSemanticMemoryGraph } from "../../src/memory/semanticMemoryGraph.js";
import { appendRuntimeJournal } from "../../src/memory/runtimeJournal.js";
import { buildSemanticGraph } from "../../src/semantic/semanticGraph.js";
import { appendSemanticJournalEvent } from "../../src/semantic/semanticJournal.js";
import { replaySemanticState } from "../../src/semantic/semanticReplay.js";
import { buildStreamTimeline } from "../../src/streaming/streamReplay.js";
import { extractVisionMetadata } from "../../src/vision/runtimeVision.js";
import { healSelector } from "../../src/adaptive/selectorHealing.js";
import { buildSemanticPatch } from "../../src/semantic/semanticPatch.js";
import { reconcileSemanticStates } from "../../src/semantic/semanticReconciliation.js";
import { restoreSemanticSnapshot } from "../../src/semantic/semanticSnapshot.js";

describe("subsystem smoke coverage", () => {
  it("connectors", async () => {
    vi.stubGlobal("fetch", vi.fn(async () => ({ ok: true }) as Response));
    expect(extractPostgresRuntime({}).bounded).toBe(true);
    expect(extractRedisRuntime({}).bounded).toBe(true);
    expect(extractKafkaRuntime({}).bounded).toBe(true);
    expect(extractFilesystemRuntime(".").bounded).toBe(true);
    expect(extractKubernetesRuntime({}).bounded).toBe(true);
    expect(extractMysqlRuntime({}).bounded).toBe(true);
    expect(extractSqliteRuntime({}).bounded).toBe(true);
    expect(extractGraphqlRuntime({}).bounded).toBe(true);
    expect(extractGrpcRuntime({}).bounded).toBe(true);
    expect(extractWebsocketRuntime({}).bounded).toBe(true);
    expect(extractDockerRuntime({}).bounded).toBe(true);
    expect(extractApiRuntime("graphql", {}).bounded).toBe(true);
    expect(extractApiRuntime("grpc", {}).bounded).toBe(true);
    expect(extractDatabaseRuntime("postgres", {}).bounded).toBe(true);
    expect(extractContainerRuntime("docker", {}).bounded).toBe(true);
    expect(extractCicdRuntime().bounded).toBe(true);
    expect(extractIdeRuntime().bounded).toBe(true);
    expect(extractTelemetryRuntime().bounded).toBe(true);
    expect(extractRuntimeStreamRuntime().bounded).toBe(true);
    const live = runLiveRuntime({ url: "https://example.com" });
    expect(live.bounded).toBe(true);
    expect(runLiveForExtraction({ url: "https://example.com" }).bounded).toBe(true);
    const dir = mkdtempSync(join(tmpdir(), "wwx-"));
    const memPath = join(dir, "m.json");
    saveLiveRuntimeMemory("mem", { ok: true }, "k", memPath);
    expect(loadLiveRuntimeMemory("mem", "k", memPath).ok).toBe(true);
    rmSync(dir, { recursive: true, force: true });
    vi.unstubAllGlobals();
  });

  it("distributed engines", () => {
    const worker = createExtractionWorker("w", {}, { profile_id: "p", fingerprint_hash: "h" }, {}, { events: [] });
    const q = enqueueExtraction([], { id: "t1" });
    expect(dequeueExtraction(q.queue).task).toBeDefined();
    expect(scheduleExtractionRuntime([{ id: "t" }], 0).bounded).toBe(true);
    expect(balanceExtractionWorkloads([worker], [{ id: "t" }]).assignments).toBeDefined();
    expect(routeAuthenticatedSessions([worker]).routes).toBeDefined();
    expect(routeBrowserIdentity([worker]).routes).toBeDefined();
    const sync = synchronizeAdaptiveRuntime([{}]);
    expect(sync.bounded).toBe(true);
    expect(sync.healed_selectors).toBeDefined();
    expect(federateStreamRuntimes([{ worker_id: "w", events: [] }]).events).toBeDefined();
    expect(federateExtractionRuntimes([]).topology).toBeDefined();
    expect(buildDistributedRuntimeGraph([worker], { nodes: [], edges: [] }).nodes).toBeDefined();
    expect(buildClusterState([worker], []).worker_count).toBe(1);
    expect(monitorExtractionCluster([worker], []).bounded).toBe(true);
    expect(recoverDistributedRuntime({ queue: [] }).recovered).toBe(true);
    expect(wwx.runDistributedExtraction([{ id: "x" }]).bounded).toBe(true);
  });

  it("semantic memory graph and journals", () => {
    const g = buildSemanticMemoryGraph(_buildRuntimeGraph({ n: 1 }));
    expect(g.bounded).toBe(true);
    expect(buildSemanticGraph([]).bounded).toBe(true);
    expect(appendSemanticJournalEvent([], { e: 1 }).length).toBeGreaterThan(0);
    expect(appendRuntimeJournal([], 0, { e: 1 }).length).toBeGreaterThan(0);
    expect(replaySemanticState({ semantic: {}, journal: [] }).replayed).toBe(true);
    const journal = wwx.createSemanticJournal();
    journal.record({ kind: "tick" });
    expect(journal.replay().count).toBe(1);
  });

  it("streaming persistence and tier B helpers", () => {
    const dir = mkdtempSync(join(tmpdir(), "wwx-stream-"));
    const path = join(dir, "stream.json");
    wwx.saveStreamRuntime(path, { events: [wwx.makeStreamEvent(0, "s", "in", "{}", "c")] }, "key");
    const loaded = wwx.loadStreamRuntime(path, "key");
    expect((loaded.events as unknown[]).length).toBe(1);
    expect(wwx.mergeStreamRuntimes(loaded, { events: [] }).events).toBeDefined();
    expect(buildStreamTimeline([wwx.makeStreamEvent(1, "a", "out", "x", "c")]).count).toBe(1);
    rmSync(dir, { recursive: true, force: true });

    expect(healSelector("#x", [{ tag: "div", text: "x", attrs: { id: "x" } }]).healed).toBeTruthy();
    expect(buildSemanticPatch({ a: 1 }, { a: 2, b: 3 }).added).toBeDefined();
    expect(reconcileSemanticStates([{ a: 1 }, { b: 2 }]).count).toBe(2);
    const snap = wwx.createSemanticSnapshot({ z: 1 });
    expect(restoreSemanticSnapshot(snap).z).toBe(1);
    expect(extractVisionMetadata({ width: 10, height: 10, format: "png" }).available).toBe(true);
    expect(wwx.replayWorkflowRuntime({ plan: {} })).toBeDefined();
    expect(wwx.detectBuildSystems([{ path: "package.json" }]).build_systems).toContain("npm");
    expect(wwx.inferFromEvidence({}, []).allowed).toBe(false);
    expect((wwx.extractCitations("doi:10.1/x").citations as unknown[]).length).toBeGreaterThan(0);
  });

  it("graph replay and browser helpers", () => {
    const graph = _buildRuntimeGraph({ a: 1 });
    expect(wwx.replayGraphLineage(graph).bounded).toBe(true);
    expect(wwx.reconstructGraphFromIr({ session: { ok: true } }).bounded).toBe(true);
    expect(wwx.computeGraphLineageFingerprint([graph]).lineage_fingerprint.length).toBeGreaterThan(0);
    expect(wwx.detectSpaFramework("<div data-reactroot></div>")).toBeTruthy();
    expect(wwx.stabilizeSpaDom("<div></div>").stabilized_html.length).toBeGreaterThan(0);
    const captured = {
      available: true,
      url: "https://example.com",
      dom_hash: "abc",
      storage: { localStorage: {}, sessionStorage: {} },
      routes: ["/"],
      network: [{ url: "https://example.com", method: "GET" }],
      bounded: true,
    };
    expect(wwx.buildBrowserIdentity(captured).runtime_identity.length).toBeGreaterThan(0);
    expect(wwx.buildMemoryLineage([{ tick: 0, kind: "init" }]).lineage.length).toBe(1);
    expect(wwx.replayMemoryState(graph, []).replay_hash).toBeDefined();
  });
});
