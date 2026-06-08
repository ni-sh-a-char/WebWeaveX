import { describe, expect, it } from "vitest";
import { existsSync } from "node:fs";
import { join } from "node:path";

describe("protected smoke: src/graph/runtimeGraphReconstruction.ts", () => {
  it("module file exists", () => {
    expect(existsSync(join(process.cwd(), "src/graph/runtimeGraphReconstruction.ts"))).toBe(true);
  });
});
