import 'runtime_action_engine.dart';
import 'runtime_permissions_engine.dart';
import 'runtime_policy_engine.dart';
import 'runtime_sandbox_engine.dart';

const Set<String> _safeTerminal = <String>{'pwd', 'echo', 'whoami'};
const Set<String> _forbiddenShell = <String>{
  'rm',
  'del',
  'format',
  'shutdown',
  'eval',
  'exec',
};

Map<String, dynamic> _normalizeAction(Map<String, dynamic> raw, int tick) {
  final String actionType = '${raw['type'] ?? raw['action_type'] ?? ''}';
  String runtime = '${raw['runtime'] ?? 'browser'}';
  Map<String, dynamic> payload;

  if (actionType == 'browser_click') {
    runtime = 'browser';
    payload = <String, dynamic>{'selector': '${raw['selector'] ?? ''}'};
  } else if (actionType == 'terminal_command') {
    runtime = 'terminal';
    payload = <String, dynamic>{'command': '${raw['command'] ?? ''}'};
  } else if (actionType == 'native_focus') {
    runtime = 'native';
    payload = <String, dynamic>{'window': '${raw['window'] ?? ''}'};
  } else {
    final dynamic pl = raw['payload'];
    payload = pl is Map
        ? <String, dynamic>{...pl.cast<String, dynamic>()}
        : <String, dynamic>{...raw};
  }

  return buildRuntimeAction(actionType, runtime, payload, tick: tick);
}

bool _actionAllowedInSandbox(
    Map<String, dynamic> sandbox, Map<String, dynamic> action) {
  final Set<dynamic> allowed = <dynamic>{
    ...((sandbox['allowed_actions'] as List<dynamic>?) ?? <dynamic>[])
  };
  return allowed.contains('${action['action_type'] ?? ''}');
}

bool _validateTerminal(String command) {
  final String trimmed = command.trim();
  final String cmd = trimmed.isEmpty ? '' : trimmed.split(RegExp(r'\s+'))[0];
  if (_forbiddenShell.contains(cmd)) return false;
  return _safeTerminal.contains(cmd);
}

/// Port of core/execution/runtime_execution_engine.execute_runtime_action.
Map<String, dynamic> executeRuntimeAction(
  Map<String, dynamic> rawAction, {
  Map<String, dynamic>? sandbox,
  Map<String, dynamic>? policy,
  Map<String, dynamic>? permissions,
  int tick = 0,
  int mutationCount = 0,
  int actionCount = 0,
}) {
  final Map<String, dynamic> sb = sandbox ?? buildRuntimeSandbox();
  final Map<String, dynamic> pol = policy ?? <String, dynamic>{};
  final Map<String, dynamic> perms = permissions ?? <String, dynamic>{};

  final Map<String, dynamic> action = _normalizeAction(rawAction, tick);
  final String runtime = '${action['runtime']}';
  final String actionType = '${action['action_type']}';

  if (!_actionAllowedInSandbox(sb, action)) {
    return <String, dynamic>{
      'executed': false,
      'action_id': action['id'],
      'runtime': runtime,
      'reason': 'sandbox_forbidden',
      'bounded': true,
    };
  }

  final Map<String, dynamic> perm =
      validateRuntimePermissions(perms, runtime, actionType);
  if (perm['allowed'] != true && perms.isNotEmpty) {
    return <String, dynamic>{
      'executed': false,
      'action_id': action['id'],
      'runtime': runtime,
      'reason': 'permission_denied',
      'bounded': true,
    };
  }

  final Map<String, dynamic> enforcement =
      enforceRuntimePolicy(pol, action, mutationCount, actionCount);
  if (enforcement['allowed'] == false) {
    return <String, dynamic>{
      'executed': false,
      'action_id': action['id'],
      'runtime': runtime,
      'reason': 'policy_violation',
      'bounded': true,
    };
  }

  if (actionType == 'terminal_command') {
    final Map<String, dynamic> pl =
        (action['payload'] as Map?)?.cast<String, dynamic>() ??
            <String, dynamic>{};
    final String command = '${pl['command'] ?? ''}';
    if (!_validateTerminal(command)) {
      return <String, dynamic>{
        'executed': false,
        'action_id': action['id'],
        'runtime': runtime,
        'reason': 'unsafe_terminal',
        'bounded': true,
      };
    }
  }

  if (actionType == 'browser_click') {
    final Map<String, dynamic> pl =
        (action['payload'] as Map?)?.cast<String, dynamic>() ??
            <String, dynamic>{};
    final dynamic selector = pl['selector'];
    if (selector == null || selector == '' || selector == false) {
      return <String, dynamic>{
        'executed': false,
        'action_id': action['id'],
        'runtime': runtime,
        'reason': 'invalid_selector',
        'bounded': true,
      };
    }
  }

  return <String, dynamic>{
    'executed': true,
    'action_id': action['id'],
    'runtime': runtime,
    'action': action,
    'bounded': true,
  };
}
