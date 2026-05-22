# LIVE CONNECTOR VALIDATION REPORT

**Generated:** 2026-05-22T17:37:09Z

```json
{
  "sqlite": {
    "bounded": true,
    "keys": [
      "database_type",
      "schemas",
      "tables",
      "indexes",
      "metrics",
      "active_connections",
      "replication_state",
      "degraded"
    ]
  },
  "postgres": {
    "bounded": true,
    "keys": [
      "database_type",
      "schemas",
      "tables",
      "indexes",
      "metrics",
      "active_connections",
      "replication_state",
      "degraded"
    ]
  },
  "redis": {
    "bounded": true,
    "keys": [
      "database_type",
      "schemas",
      "tables",
      "indexes",
      "metrics",
      "active_connections",
      "replication_state",
      "streams"
    ]
  },
  "api_rest": {
    "bounded": true,
    "keys": [
      "api_type",
      "endpoints",
      "schemas",
      "auth_state",
      "rate_limits",
      "response_topology",
      "pagination_models",
      "bounded"
    ]
  },
  "api_graphql": {
    "bounded": true,
    "keys": [
      "api_type",
      "endpoints",
      "schemas",
      "auth_state",
      "rate_limits",
      "response_topology",
      "pagination_models",
      "bounded"
    ]
  },
  "streams": {
    "bounded": true,
    "keys": [
      "streams",
      "count",
      "bounded"
    ]
  },
  "docker": {
    "bounded": true,
    "keys": [
      "runtime",
      "containers",
      "images",
      "volumes",
      "networks",
      "states",
      "health",
      "degraded"
    ]
  },
  "k8s": {
    "bounded": true,
    "keys": [
      "namespaces",
      "pods",
      "deployments",
      "services",
      "ingress",
      "topology",
      "events",
      "degraded"
    ]
  },
  "otel": {
    "bounded": true,
    "keys": [
      "backends",
      "metrics",
      "traces",
      "spans",
      "logs",
      "distributed_correlations",
      "degraded",
      "bounded"
    ]
  }
}
```