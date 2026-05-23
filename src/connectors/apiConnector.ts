import { extractGraphqlRuntime } from "./graphqlConnector.js";
import { extractGrpcRuntime } from "./grpcConnector.js";

export function extractApiRuntime(
  apiType = "rest",
  snapshot: Record<string, unknown> = {},
): Record<string, unknown> {
  const normalized = apiType.toLowerCase();
  const base: Record<string, unknown> = {
    api_type: normalized,
    endpoints: [...((snapshot.endpoints as unknown[]) ?? [])].map(String).sort(),
    schemas: [...((snapshot.schemas as unknown[]) ?? [])],
    auth_state: { ...(snapshot.auth as Record<string, unknown>) },
    rate_limits: { ...(snapshot.rate_limits as Record<string, unknown>) },
    response_topology: [...((snapshot.responses as unknown[]) ?? [])],
    pagination_models: [...((snapshot.pagination as unknown[]) ?? [])],
    bounded: true,
  };
  if (normalized === "graphql") return { ...base, ...extractGraphqlRuntime(snapshot) };
  if (normalized === "grpc") return { ...base, ...extractGrpcRuntime(snapshot) };
  return base;
}
