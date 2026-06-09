/// Port of core/connectors/api_connector_engine.extract_api_runtime
/// plus the graphql/grpc sub-engines it delegates to.
library;

/// Port of core/connectors/graphql_connector_engine.extract_graphql_runtime.
Map<String, dynamic> extractGraphqlRuntime([Map<String, dynamic>? snapshot]) {
  final Map<String, dynamic> snap = snapshot ?? <String, dynamic>{};
  final List<dynamic> types =
      List<dynamic>.from(snap['types'] as List<dynamic>? ?? <dynamic>[]);
  types.sort((dynamic a, dynamic b) => '$a'.compareTo('$b'));
  return <String, dynamic>{
    'protocol': 'graphql',
    'endpoints': List<dynamic>.from(
        snap['endpoints'] as List<dynamic>? ?? <dynamic>['/graphql']),
    'schemas':
        List<dynamic>.from(snap['schemas'] as List<dynamic>? ?? <dynamic>[]),
    'types': types,
    'bounded': true,
  };
}

/// Port of core/connectors/grpc_connector_engine.extract_grpc_runtime.
Map<String, dynamic> extractGrpcRuntime([Map<String, dynamic>? snapshot]) {
  final Map<String, dynamic> snap = snapshot ?? <String, dynamic>{};
  final List<dynamic> services =
      List<dynamic>.from(snap['services'] as List<dynamic>? ?? <dynamic>[]);
  services.sort((dynamic a, dynamic b) => '$a'.compareTo('$b'));
  final List<dynamic> methods =
      List<dynamic>.from(snap['methods'] as List<dynamic>? ?? <dynamic>[]);
  methods.sort((dynamic a, dynamic b) => '$a'.compareTo('$b'));
  return <String, dynamic>{
    'protocol': 'grpc',
    'services': services,
    'methods': methods,
    'schemas':
        List<dynamic>.from(snap['protobuf'] as List<dynamic>? ?? <dynamic>[]),
    'bounded': true,
  };
}

/// Port of core/connectors/api_connector_engine.extract_api_runtime.
Map<String, dynamic> extractApiRuntime({
  String apiType = 'rest',
  Map<String, dynamic>? snapshot,
}) {
  final Map<String, dynamic> snap = snapshot ?? <String, dynamic>{};
  final String normalized = apiType.toLowerCase();

  final List<dynamic> endpoints =
      List<dynamic>.from(snap['endpoints'] as List<dynamic>? ?? <dynamic>[]);
  endpoints.sort((dynamic a, dynamic b) => '$a'.compareTo('$b'));

  final Map<String, dynamic> base = <String, dynamic>{
    'api_type': normalized,
    'endpoints': endpoints,
    'schemas':
        List<dynamic>.from(snap['schemas'] as List<dynamic>? ?? <dynamic>[]),
    'auth_state': Map<String, dynamic>.from(
        (snap['auth'] as Map<dynamic, dynamic>?) ?? <dynamic, dynamic>{}),
    'rate_limits': Map<String, dynamic>.from(
        (snap['rate_limits'] as Map<dynamic, dynamic>?) ??
            <dynamic, dynamic>{}),
    'response_topology':
        List<dynamic>.from(snap['responses'] as List<dynamic>? ?? <dynamic>[]),
    'pagination_models':
        List<dynamic>.from(snap['pagination'] as List<dynamic>? ?? <dynamic>[]),
    'bounded': true,
  };

  if (normalized == 'graphql') {
    base['graphql'] =
        extractGraphqlRuntime(snap['graphql'] as Map<String, dynamic>?);
  } else if (normalized == 'grpc') {
    base['grpc'] = extractGrpcRuntime(snap['grpc'] as Map<String, dynamic>?);
  }

  return base;
}
