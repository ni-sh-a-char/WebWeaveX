/// Port of core/execution/runtime_permissions_engine.
const List<String> _scopes = <String>[
  'browser',
  'native',
  'filesystem',
  'connector',
  'terminal',
  'vm',
];

Map<String, dynamic> buildRuntimePermissions({List<String>? scopes}) {
  final List<String> active = (<String>{
    ...(scopes ?? <String>['browser', 'native'])
  }.toList())
    ..sort();
  final Map<String, dynamic> scopeMap = <String, dynamic>{};
  for (final String scope in _scopes) {
    scopeMap[scope] = active.contains(scope);
  }
  return <String, dynamic>{
    'scopes': scopeMap,
    'active_scopes': active,
    'bounded': true,
  };
}

Map<String, dynamic> validateRuntimePermissions(
  Map<String, dynamic> permissions,
  String runtime,
  String actionType,
) {
  final Map<String, dynamic> scopes =
      (permissions['scopes'] as Map<String, dynamic>?) ?? <String, dynamic>{};
  String runtimeScope = _scopes.contains(runtime) ? runtime : 'browser';

  if (actionType.startsWith('terminal_') || actionType == 'terminal_command') {
    runtimeScope = 'terminal';
  } else if (actionType.startsWith('native_')) {
    runtimeScope = 'native';
  } else if (actionType.startsWith('vm_')) {
    runtimeScope = 'vm';
  } else if (actionType.startsWith('connector_')) {
    runtimeScope = 'connector';
  }

  final bool allowed = scopes[runtimeScope] == true;
  return <String, dynamic>{
    'allowed': allowed,
    'scope': runtimeScope,
    'deterministic': true,
    'bounded': true,
  };
}
