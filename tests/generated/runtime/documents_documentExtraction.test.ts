import { describe, expect, it } from "vitest";
import { existsSync } from "node:fs";
import { join } from "node:path";

describe("protected smoke: src/documents/documentExtraction.ts", () => {
  it("module file exists", () => {
    expect(existsSync(join(process.cwd(), "src/documents/documentExtraction.ts"))).toBe(true);
  });
});
