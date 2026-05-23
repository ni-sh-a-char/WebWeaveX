import { describe, expect, it } from "vitest";
import { computeStableDomHash } from "../../src/determinism/domStabilization.js";
import { computeGlobalRuntimeFingerprint } from "../../src/determinism/globalRuntimeFingerprint.js";

describe("determinism", () => {
  it("stable dom hash", () => {
    const h1 = computeStableDomHash("<div>test</div>");
    const h2 = computeStableDomHash("<div>test</div>");
    expect(h1).toBe(h2);
  });

  it("global fingerprint stable", () => {
    const fp1 = computeGlobalRuntimeFingerprint({ pipeline_hash: "a" });
    const fp2 = computeGlobalRuntimeFingerprint({ pipeline_hash: "a" });
    expect(fp1).toBe(fp2);
  });
});
