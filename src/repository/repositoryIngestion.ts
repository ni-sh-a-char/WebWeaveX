import { existsSync, statSync } from "node:fs";
import { resolve } from "node:path";

export function ingestRepository(path: string): Record<string, unknown> {
  const abs = resolve(path);
  const available = existsSync(abs);
  const isDir = available && statSync(abs).isDirectory();
  return {
    available,
    bounded: true,
    path: abs,
    kind: isDir ? "repository" : "path",
    input_type: "filesystem",
  };
}
