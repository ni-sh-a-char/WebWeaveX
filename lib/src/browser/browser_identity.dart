import '../crypto/kaalka_runtime.dart';

Map<String, dynamic> buildBrowserIdentityFromCapture(
    Map<String, dynamic> captured) {
  final storageHash =
      computeDeterministicHash(captured['storage'] ?? <String, dynamic>{});
  final routeFingerprint =
      computeDeterministicHash({'routes': captured['routes'] ?? <dynamic>[]});
  final runtimeIdentity = computeDeterministicHash({
    'url': captured['url'],
    'dom_hash': captured['dom_hash'],
    'storage_hash': storageHash,
    'route_fingerprint': routeFingerprint,
  });
  return {
    'runtime_identity': runtimeIdentity,
    'profile_hash': computeDeterministicHash({
      'url': captured['url'],
      'network_len': (captured['network'] as List?)?.length ?? 0,
    }),
    'storage_hash': storageHash,
    'route_fingerprint': routeFingerprint,
    'bounded': true,
  };
}

Map<String, dynamic> identityFromExtraction(Map<String, dynamic> envelope) {
  final ir = envelope['browser_ir'] as Map? ?? {};
  return {
    'runtime_identity': ir['runtime_identity'] ?? '',
    'profile_hash': computeDeterministicHash(
        {'storage': ir['storage'] ?? <String, dynamic>{}}),
    'storage_hash':
        computeDeterministicHash(ir['storage'] ?? <String, dynamic>{}),
    'route_fingerprint': computeDeterministicHash(envelope),
    'bounded': true,
  };
}
