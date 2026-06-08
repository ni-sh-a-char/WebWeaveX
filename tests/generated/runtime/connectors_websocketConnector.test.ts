import { describe, expect, it } from "vitest";
import { existsSync } from "node:fs";
import { join } from "node:path";

describe("protected smoke: src/connectors/websocketConnector.ts", () => {
  it("module file exists", () => {
    expect(existsSync(join(process.cwd(), "src/connectors/websocketConnector.ts"))).toBe(true);
  });
});
