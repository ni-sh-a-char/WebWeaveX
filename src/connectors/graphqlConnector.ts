export function extractGraphqlRuntime(snapshot: Record<string, unknown> = {}): Record<string, unknown> {
  return {
    protocol: "graphql",
    endpoints: [...((snapshot.endpoints as unknown[]) ?? ["/graphql"])],
    schemas: [...((snapshot.schemas as unknown[]) ?? [])],
    types: [...((snapshot.types as unknown[]) ?? [])].map(String).sort(),
    bounded: true,
  };
}
