export function extractWebsocketRuntime(snapshot: Record<string, unknown> = {}): Record<string, unknown> {
  return {
    protocol: "websocket",
    connections: [...((snapshot.connections as unknown[]) ?? [])],
    frames: Number(snapshot.frames ?? 0),
    bounded: true,
  };
}
