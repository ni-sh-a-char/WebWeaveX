import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { describe, expect, it } from "vitest";
import { decryptValue, encryptValue } from "../../src/crypto/kaalkaRuntime.js";

const root = join(dirname(fileURLToPath(import.meta.url)), "../..");
const vectors = JSON.parse(
  readFileSync(join(root, "validation/kaalka/js_vectors.json"), "utf-8"),
) as { vectors: Array<{ id: string; encrypted: string; key?: string; plaintext?: string }> };

describe("Kaalka via npm + WebWeaveX normalization", () => {
  it("deterministic encrypt", () => {
    const a = encryptValue("probe", "k");
    const b = encryptValue("probe", "k");
    expect(a.encrypted).toBe(b.encrypted);
    expect(decryptValue(a.encrypted, "k").decrypted).toBe("probe");
  });

  for (const v of vectors.vectors.filter((x) => x.id === "probe-1")) {
    it(`vector ${v.id}`, () => {
      expect(v.encrypted.length).toBeGreaterThan(0);
    });
  }
});
