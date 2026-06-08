import { readFileSync } from "node:fs";
import { defineConfig } from "vitest/config";

const protectedModules = readFileSync("tools/convergence/protected_js.txt", "utf-8")
  .split(/\r?\n/)
  .map((l) => l.trim())
  .filter((l) => l.startsWith("src/") && l.endsWith(".ts"));

export default defineConfig({
  test: {
    environment: "node",
    include: ["tests/**/*.test.ts"],
    testTimeout: 60000,
    coverage: {
      provider: "v8",
      reporter: ["text", "json-summary"],
      include: protectedModules.length ? protectedModules : ["src/**/*.ts"],
      exclude: ["src/contracts/runtimeContracts.ts"],
      thresholds: { lines: 98, functions: 98, branches: 95, statements: 98 },
    },
  },
});