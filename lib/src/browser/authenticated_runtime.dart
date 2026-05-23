import 'dart:convert';
import 'dart:io';

import '../crypto/kaalka_runtime.dart';

Map<String, dynamic> saveAuthenticatedRuntime(
  String path,
  Map<String, dynamic> session,
  String encryptionKey,
) {
  final encrypted = encryptValue(session, encryptionKey);
  File(path).writeAsStringSync(jsonEncode({'encrypted': encrypted}));
  return {'saved': true, 'path': path, 'bounded': true};
}

Map<String, dynamic> loadAuthenticatedRuntime(
    String path, String encryptionKey) {
  final raw = File(path).readAsStringSync();
  final wrapper = jsonDecode(raw) as Map<String, dynamic>;
  final enc = wrapper['encrypted'] as String;
  final decrypted = decryptValue(enc, encryptionKey);
  if (decrypted is Map<String, dynamic>) return decrypted;
  return jsonDecode(decrypted as String) as Map<String, dynamic>;
}

Map<String, dynamic> rotateAuthenticatedSession(
  String path,
  String oldKey,
  String newKey,
) {
  final session = loadAuthenticatedRuntime(path, oldKey);
  return saveAuthenticatedRuntime(path, session, newKey);
}
