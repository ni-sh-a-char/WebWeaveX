import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { describe, expect, it } from "vitest";
import { decryptValue, encryptValue } from "kaalka";

const root = join(dirname(fileURLToPath(import.meta.url)), "../..");
const vectors = JSON.parse(
  readFileSync(join(root, "validation/kaalka/reference_vectors.json"), "utf-8"),
) as { vectors: Array<{ id: string; plaintext: string; key: string; encrypted: string }> };

describe("Kaalka parity", () => {
  for (const v of vectors.vectors) {
    it(`encrypt ${v.id}`, () => {
      const out = encryptValue(v.plaintext, v.key);
      expect(out.encrypted).toBe(v.encrypted);
      expect(decryptValue(out.encrypted, v.key).decrypted).toBe(v.plaintext);
    });
  }

  it("deterministic repeat", () => {
    const a = encryptValue("probe", "k");
    const b = encryptValue("probe", "k");
    expect(a.encrypted).toBe(b.encrypted);
  });
});
