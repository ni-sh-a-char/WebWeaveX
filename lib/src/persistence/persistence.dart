// Family barrel: WebWeaveX persistence + crypto-session public APIs (Dart).
// Mirrors the Python webweavex.__all__ persistence subset with camelCase names.

export 'fingerprint_hex.dart' show hexFingerprint, dumpsDeterministic;
export 'persistence_runtime.dart'
    show
        encryptSessionState,
        decryptSessionState,
        saveEncryptedSession,
        loadEncryptedSession,
        saveBrowserIdentity,
        loadBrowserIdentity,
        saveAdaptiveMemory,
        loadAdaptiveMemory,
        saveDistributedCheckpoint,
        loadDistributedCheckpoint,
        saveLiveRuntime,
        loadLiveRuntime,
        authenticateRuntime,
        AuthPageStub;

import 'fingerprint_hex.dart' as fp;

/// Public Python `fingerprint` (= hex_fingerprint).
String fingerprint(dynamic payload, [String token = 'webweavex']) =>
    fp.hexFingerprint(payload, token);
