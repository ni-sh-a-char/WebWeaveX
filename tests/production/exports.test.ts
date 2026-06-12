import { describe, expect, it } from "vitest";
import * as wwx from "../../src/index.js";

describe("public exports", () => {
  it("VERSION and core APIs", () => {
    expect(wwx.VERSION).toBe("2.1.0");
    expect(typeof wwx.extractWeb).toBe("function");
    expect(typeof wwx.runCanonicalPipeline).toBe("function");
    expect(typeof wwx.validateReplayEquivalence).toBe("function");
    expect(typeof wwx.encryptValue).toBe("function");
  });
});
