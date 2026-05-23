export function extractIdeRuntime(
  ide = "vscode",
  snapshot: Record<string, unknown> = {},
): Record<string, unknown> {
  return {
    ide,
    open_files: [...((snapshot.open_files as unknown[]) ?? [])].map(String).sort(),
    terminals: [...((snapshot.terminals as unknown[]) ?? [])],
    tabs: [...((snapshot.tabs as unknown[]) ?? [])],
    workspace_topology: { ...(snapshot.workspace as Record<string, unknown>) },
    debug_sessions: [...((snapshot.debug_sessions as unknown[]) ?? [])],
    degraded: Boolean(snapshot.degraded ?? false),
    bounded: true,
  };
}
