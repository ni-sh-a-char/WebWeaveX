import { describe, expect, it } from "vitest";
import { existsSync } from "node:fs";
import { join } from "node:path";

describe("protected smoke: src/parsers/parserOrchestration.ts", () => {
  it("module file exists", () => {
    expect(existsSync(join(process.cwd(), "src/parsers/parserOrchestration.ts"))).toBe(true);
  });
});
