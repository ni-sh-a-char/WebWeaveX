import { readdirSync, statSync, existsSync } from "node:fs";
import { join, relative } from "node:path";

/** Port of core/connectors/filesystem_connector_engine.py */
export function extractFilesystemRuntime(
  root = ".",
  snapshot?: Record<string, unknown>,
): Record<string, unknown> {
  if (snapshot) {
    return {
      root: String(snapshot.root ?? root),
      topology: [...((snapshot.files as unknown[]) ?? [])].map(String).sort(),
      mutation_streams: [...((snapshot.mutations as unknown[]) ?? [])],
      synchronization_state: { ...((snapshot.sync as Record<string, unknown>) ?? {}) },
      permissions: { ...((snapshot.permissions as Record<string, unknown>) ?? {}) },
      inode_relationships: [...((snapshot.inodes as unknown[]) ?? [])],
      bounded: true,
    };
  }

  const topology: string[] = [];
  try {
    if (existsSync(root)) {
      const walk = (dir: string, depth: number): void => {
        if (topology.length >= 5000 || depth > 8) return;
        for (const entry of readdirSync(dir).sort()) {
          const full = join(dir, entry);
          if (statSync(full).isFile()) {
            topology.push(relative(root, full));
          } else if (statSync(full).isDirectory()) {
            walk(full, depth + 1);
          }
        }
      };
      walk(root, 0);
    }
  } catch {
    return { root, topology: [], degraded: true, bounded: true };
  }

  return {
    root,
    topology,
    mutation_streams: [],
    synchronization_state: {},
    permissions: {},
    inode_relationships: [],
    bounded: true,
  };
}
