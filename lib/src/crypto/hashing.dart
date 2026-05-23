import 'dart:convert';

import 'package:crypto/crypto.dart';

import '../determinism/stable_serialize.dart';

String computeDeterministicHash(dynamic value) {
  final payload = stableSerialize(value);
  return sha256.convert(utf8.encode(payload)).toString();
}
