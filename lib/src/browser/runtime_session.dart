import '../crypto/kaalka_runtime.dart';
import 'authenticated_runtime.dart';

Map<String, dynamic> createRuntimeSession([Map<String, dynamic>? state]) {
  final s = state ?? {};
  final session = {
    'cookies': s['cookies'] ?? <dynamic>[],
    'headers': s['headers'] ?? <String, dynamic>{},
    'auth_tokens': s['auth_tokens'] ?? <dynamic>[],
    'localStorage': s['localStorage'] ?? <String, dynamic>{},
    'sessionStorage': s['sessionStorage'] ?? <String, dynamic>{},
  };
  return {
    ...session,
    'session_id': computeDeterministicHash(session),
    'bounded': true,
  };
}

Map<String, dynamic> persistRuntimeSession(
  String path,
  Map<String, dynamic> session,
  String encryptionKey,
) {
  saveAuthenticatedRuntime(path, session, encryptionKey);
  return {'path': path, 'session_id': session['session_id'], 'bounded': true};
}

Map<String, dynamic> restoreRuntimeSession(String path, String encryptionKey) =>
    createRuntimeSession(loadAuthenticatedRuntime(path, encryptionKey));
