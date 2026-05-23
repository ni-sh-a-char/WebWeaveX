import { describe, expect, it } from "vitest";
import {
  normalizeRuntimeValue,
  stableSerialize,
  stableSortKeys,
} from "../../src/determinism/normalization.js";
import { computeDeterministicHash } from "../../src/crypto/kaalkaRuntime.js";

describe("normalization pipeline", () => {
  it("NFKC and CRLF", () => {
    expect(normalizeRuntimeValue("a\r\n")).toBe("a");
  });

  it("stable serialize + hash", () => {
    const h1 = computeDeterministicHash({ z: 1, a: 2 });
    const h2 = computeDeterministicHash({ a: 2, z: 1 });
    expect(h1).toBe(h2);
    expect(stableSerialize({ b: 1, a: 2 })).toBe(stableSerialize(stableSortKeys({ b: 1, a: 2 })));
  });
});
