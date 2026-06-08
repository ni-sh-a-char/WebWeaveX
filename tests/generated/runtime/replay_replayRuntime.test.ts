import { describe, expect, it } from "vitest";
import { existsSync } from "node:fs";
import { join } from "node:path";

describe("protected smoke: src/replay/replayRuntime.ts", () => {
  it("module file exists", () => {
    expect(existsSync(join(process.cwd(), "src/replay/replayRuntime.ts"))).toBe(true);
  });
});
