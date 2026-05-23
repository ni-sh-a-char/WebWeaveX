export function extractGrpcRuntime(snapshot: Record<string, unknown> = {}): Record<string, unknown> {
  return {
    protocol: "grpc",
    services: [...((snapshot.services as unknown[]) ?? [])].map(String).sort(),
    methods: [...((snapshot.methods as unknown[]) ?? [])].map(String).sort(),
    schemas: [...((snapshot.protobuf as unknown[]) ?? [])],
    bounded: true,
  };
}
