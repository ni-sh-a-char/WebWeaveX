import { extractPostgresRuntime, extractRedisRuntime, runLiveRuntime } from "../../src/connectors/index.js";

const pg = extractPostgresRuntime({ tables: ["users"], schemas: ["public"] });
const redis = extractRedisRuntime({ keys: ["a", "b"] });
const live = runLiveRuntime({ database_type: "postgresql" });

const results = {
  postgres: pg.database_type === "postgresql",
  redis: redis.database_type === "redis",
  live: live.bounded === true,
};

console.log("PASS", results);
if (!Object.values(results).every(Boolean)) process.exit(1);
