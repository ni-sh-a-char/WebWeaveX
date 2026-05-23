import { describe, expect, it } from "vitest";
import * as runtime from "../../src/crypto/kaalkaRuntime.js";

describe("kaalkaRuntime adapter", () => {
  it("re-exports kaalka API", () => {
    expect(runtime.encryptValue("a", "k").deterministic).toBe(true);
    expect(runtime.computeKaalkaHash("x")).toBe(runtime.computeDeterministicHash("x"));
    expect(runtime.computeKaalkaHashPayload({ a: 1 })).toHaveLength(64);
  });
});
