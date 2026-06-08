import { describe, expect, it } from "vitest";
import { extractGraphqlRuntime } from "../../src/connectors/graphqlConnector.js";
import { extractGrpcRuntime } from "../../src/connectors/grpcConnector.js";
import { extractKafkaRuntime } from "../../src/connectors/kafkaConnector.js";
import { extractRedisRuntime } from "../../src/connectors/redisConnector.js";
import { extractPostgresRuntime } from "../../src/connectors/postgresConnector.js";
import { extractMysqlRuntime } from "../../src/connectors/mysqlConnector.js";
import { extractSqliteRuntime } from "../../src/connectors/sqliteConnector.js";
import { extractWebsocketRuntime } from "../../src/connectors/websocketConnector.js";
import { extractDockerRuntime } from "../../src/connectors/dockerConnector.js";
import { extractKubernetesRuntime } from "../../src/connectors/kubernetesConnector.js";
import { extractFilesystemRuntime } from "../../src/connectors/filesystemConnector.js";
import { extractCicdRuntime } from "../../src/connectors/cicdConnector.js";
import { extractIdeRuntime } from "../../src/connectors/ideConnector.js";
import { extractTelemetryRuntime } from "../../src/connectors/telemetryConnector.js";
import { extractRuntimeStreamRuntime } from "../../src/connectors/runtimeStreamConnector.js";
import { extractApiRuntime } from "../../src/connectors/apiConnector.js";
import { extractDatabaseRuntime } from "../../src/connectors/databaseConnector.js";
import { extractContainerRuntime } from "../../src/connectors/containerConnector.js";
import { runLiveRuntime } from "../../src/connectors/liveRuntimeOrchestrator.js";

describe("connector snapshot branches", () => {
  const snap = {
    endpoints: ["/v1"],
    schemas: [{ name: "User" }],
    types: ["Query"],
    workflows: [{ id: "w1" }],
    jobs: [{ id: "j1" }],
    logs: ["line"],
    artifacts: ["a.zip"],
    open_files: ["main.ts"],
    terminals: [{ id: "t1" }],
    tabs: [{ id: "tab1" }],
    workspace: { root: "." },
    metrics: [{ m: 1 }],
    traces: [{ t: 1 }],
    spans: [{ s: 1 }],
    correlations: [{ c: 1 }],
    kafka: { topics: ["t"] },
    redis: { keys: ["k"] },
  };

  it("all connectors with rich snapshots", () => {
    expect(extractGraphqlRuntime(snap).bounded).toBe(true);
    expect(extractGrpcRuntime(snap).bounded).toBe(true);
    expect(extractKafkaRuntime(snap).bounded).toBe(true);
    expect(extractRedisRuntime(snap).bounded).toBe(true);
    expect(extractPostgresRuntime(snap).bounded).toBe(true);
    expect(extractMysqlRuntime(snap).bounded).toBe(true);
    expect(extractSqliteRuntime(snap).bounded).toBe(true);
    expect(extractWebsocketRuntime(snap).bounded).toBe(true);
    expect(extractDockerRuntime(snap).bounded).toBe(true);
    expect(extractKubernetesRuntime(snap).bounded).toBe(true);
    expect(extractFilesystemRuntime(".").bounded).toBe(true);
    expect(extractCicdRuntime("github_actions", snap).bounded).toBe(true);
    expect(extractIdeRuntime("vscode", snap).bounded).toBe(true);
    expect(extractTelemetryRuntime(["prometheus"], snap).bounded).toBe(true);
    expect(extractRuntimeStreamRuntime(["kafka", "redis", "websocket"], snap).bounded).toBe(true);
    expect(extractApiRuntime("rest", snap).bounded).toBe(true);
    expect(extractDatabaseRuntime("mysql", snap).bounded).toBe(true);
    expect(extractContainerRuntime("podman", snap).bounded).toBe(true);
    expect(runLiveRuntime({ save_path: undefined }).bounded).toBe(true);
  });
});
