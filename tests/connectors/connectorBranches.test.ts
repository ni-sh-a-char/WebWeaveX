import { describe, expect, it } from "vitest";
import { extractDatabaseRuntime } from "../../src/connectors/databaseConnector.js";
import { extractContainerRuntime } from "../../src/connectors/containerConnector.js";
import { extractApiRuntime } from "../../src/connectors/apiConnector.js";
describe("connector branch coverage", () => {
  it("database unknown type degrades", () => {
    expect(extractDatabaseRuntime("cockroach", {}).degraded).toBe(true);
  });

  it("container unknown runtime degrades", () => {
    expect(extractContainerRuntime("lxc", {}).degraded).toBe(true);
  });

  it("api rest base path", () => {
    expect(extractApiRuntime("rest", { endpoints: ["/v1"] }).api_type).toBe("rest");
  });

});
