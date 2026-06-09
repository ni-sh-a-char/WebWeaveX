// Faithful Dart ports of the WebWeaveX persistence + crypto-session public APIs:
//   core/crypto/kaalka_session_engine.py        encrypt_session_state / decrypt_session_state
//   core/session/encrypted_session_store.py      save/load_encrypted_session
//   core/identity/fingerprint_persistence_engine.py  save/load_browser_identity
//   core/adaptive/extraction_memory_engine.py    save/load_adaptive_memory
//   core/distributed_extraction/distributed_checkpoint_engine.py save/load_distributed_checkpoint
//   core/connectors/live_runtime_memory_engine.py save/load_live_runtime
//   core/auth/authentication_runtime_engine.py   authenticate_runtime

import 'dart:convert';
import 'dart:io';

import '../crypto/kaalka_runtime.dart' show encryptValue, decryptValue;

const _maxSessionBytes = 10000000;

// ---------------------------------------------------------------------------
// JSON helpers mirroring Python's json.dumps variants exactly.
// ---------------------------------------------------------------------------

/// `json.dumps(value, sort_keys=True, separators=(",",":"), ensure_ascii=False)`.
String _compactSorted(dynamic value) {
  final v = _deepSortKeys(value);
  return _CompactJsonEncoder().convert(v);
}

/// `json.dumps(value, sort_keys=True)` — Python default separators (", ", ": ").
String _pyJsonSortKeys(dynamic value) {
  final v = _deepSortKeys(value);
  return _PyJsonEncoder().convert(v);
}

dynamic _deepSortKeys(dynamic value) {
  if (value is Map) {
    final out = <String, dynamic>{};
    final keys = value.keys.map((k) => k.toString()).toList()..sort();
    for (final k in keys) {
      out[k] = _deepSortKeys(value[k]);
    }
    return out;
  }
  if (value is List) {
    return value.map(_deepSortKeys).toList();
  }
  return value;
}

class _CompactJsonEncoder {
  String convert(dynamic value) {
    final buf = StringBuffer();
    _write(value, buf);
    return buf.toString();
  }

  void _write(dynamic value, StringBuffer buf) {
    if (value is Map) {
      buf.write('{');
      var first = true;
      value.forEach((k, v) {
        if (!first) buf.write(',');
        first = false;
        buf.write(jsonEncode(k.toString()));
        buf.write(':');
        _write(v, buf);
      });
      buf.write('}');
    } else if (value is List) {
      buf.write('[');
      var first = true;
      for (final v in value) {
        if (!first) buf.write(',');
        first = false;
        _write(v, buf);
      }
      buf.write(']');
    } else {
      buf.write(jsonEncode(value));
    }
  }
}

class _PyJsonEncoder {
  String convert(dynamic value) {
    final buf = StringBuffer();
    _write(value, buf);
    return buf.toString();
  }

  void _write(dynamic value, StringBuffer buf) {
    if (value is Map) {
      buf.write('{');
      var first = true;
      value.forEach((k, v) {
        if (!first) buf.write(', ');
        first = false;
        buf.write(jsonEncode(k.toString()));
        buf.write(': ');
        _write(v, buf);
      });
      buf.write('}');
    } else if (value is List) {
      buf.write('[');
      var first = true;
      for (final v in value) {
        if (!first) buf.write(', ');
        first = false;
        _write(v, buf);
      }
      buf.write(']');
    } else {
      buf.write(jsonEncode(value));
    }
  }
}

// ---------------------------------------------------------------------------
// core/crypto/kaalka_session_engine.py
// ---------------------------------------------------------------------------

/// Port of `encrypt_session_state(session, key)`.
Map<String, dynamic> encryptSessionState(
  Map<String, dynamic> session,
  String key,
) {
  var serialized = _compactSorted(session);
  if (serialized.length > _maxSessionBytes) {
    serialized = serialized.substring(0, _maxSessionBytes);
  }
  // encrypt_value returns an envelope dict; we spread it then add fields.
  final encrypted = <String, dynamic>{
    'encrypted': encryptValue(serialized, key),
    'algorithm': 'webweavex-formula+kaalka@5.0.0',
    'deterministic': true,
    'bounded': true,
  };
  return <String, dynamic>{
    ...encrypted,
    'payload_type': 'session',
    'bounded': true,
  };
}

/// Port of `decrypt_session_state(payload, key)`.
Map<String, dynamic> decryptSessionState(
  Map<String, dynamic> payload,
  String key,
) {
  final ciphertext = (payload['encrypted'] ?? '').toString();
  // Python decrypt_value(...)["decrypted"] is always the UTF-8 string.
  final raw = decryptValue(ciphertext, key);
  final text = raw is String ? raw : _compactSorted(raw);
  final bounded = text.length > _maxSessionBytes
      ? text.substring(0, _maxSessionBytes)
      : text;
  final session = jsonDecode(bounded);
  return <String, dynamic>{
    'session': session,
    'algorithm': 'kaalka',
    'deterministic': true,
    'bounded': true,
  };
}

// ---------------------------------------------------------------------------
// File save/load helpers built on encrypt_session_state.
// ---------------------------------------------------------------------------

Map<String, dynamic> _saveSessionEnvelope(
  String path,
  Map<String, dynamic> state,
  String key,
) {
  final encrypted = encryptSessionState(state, key);
  final target = File(path);
  target.parent.createSync(recursive: true);
  target.writeAsStringSync(_pyJsonSortKeys(encrypted));
  return <String, dynamic>{
    'saved': true,
    'path': target.path,
    'algorithm': 'kaalka',
    'bounded': true,
  };
}

Map<String, dynamic> _loadSessionEnvelope(String path, String key) {
  final encrypted =
      jsonDecode(File(path).readAsStringSync()) as Map<String, dynamic>;
  return decryptSessionState(encrypted, key);
}

// ---------------------------------------------------------------------------
// core/session/encrypted_session_store.py
// ---------------------------------------------------------------------------

/// Port of `save_encrypted_session(path, session, key)`.
Map<String, dynamic> saveEncryptedSession(
  String path,
  Map<String, dynamic> session,
  String key,
) =>
    _saveSessionEnvelope(path, session, key);

/// Port of `load_encrypted_session(path, key)`.
Map<String, dynamic> loadEncryptedSession(String path, String key) {
  final target = File(path);
  if (!target.existsSync()) {
    return <String, dynamic>{
      'available': false,
      'session': <String, dynamic>{
        'cookies': <dynamic>[],
        'headers': <String, dynamic>{},
        'auth_tokens': <dynamic>[],
        'local_storage': <String, dynamic>{},
        'session_storage': <String, dynamic>{},
        'authenticated': false,
        'bounded': true,
      },
      'bounded': true,
    };
  }

  Map<String, dynamic> payload;
  try {
    payload = jsonDecode(target.readAsStringSync()) as Map<String, dynamic>;
  } catch (exc) {
    var reason = exc.toString();
    if (reason.length > 200) reason = reason.substring(0, 200);
    return <String, dynamic>{
      'available': false,
      'reason': reason,
      'session': <String, dynamic>{
        'cookies': <dynamic>[],
        'headers': <String, dynamic>{},
        'auth_tokens': <dynamic>[],
        'bounded': true,
      },
      'bounded': true,
    };
  }

  final decrypted = decryptSessionState(payload, key);
  return <String, dynamic>{
    'available': true,
    'session': decrypted['session'] ?? <String, dynamic>{},
    'algorithm': 'kaalka',
    'bounded': true,
  };
}

// ---------------------------------------------------------------------------
// core/identity/fingerprint_persistence_engine.py
// ---------------------------------------------------------------------------

/// Port of `save_browser_identity(path, identity, key)`.
Map<String, dynamic> saveBrowserIdentity(
  String path,
  Map<String, dynamic> identity,
  String key,
) =>
    _saveSessionEnvelope(path, identity, key);

/// Port of `load_browser_identity(path, key)`.
///
/// The missing-file branch in Python returns build_browser_identity("default");
/// here we expose the absence and an empty identity (a real browser-identity
/// build is out of scope for this persistence family — see report).
Map<String, dynamic> loadBrowserIdentity(String path, String key) {
  if (!File(path).existsSync()) {
    return <String, dynamic>{
      'available': false,
      'identity': <String, dynamic>{},
      'bounded': true,
    };
  }
  final decrypted = _loadSessionEnvelope(path, key);
  return <String, dynamic>{
    'available': true,
    'identity': decrypted['session'] ?? <String, dynamic>{},
    'algorithm': 'kaalka',
    'bounded': true,
  };
}

// ---------------------------------------------------------------------------
// core/adaptive/extraction_memory_engine.py
// ---------------------------------------------------------------------------

/// Port of `save_adaptive_memory(path, memory, key)`.
Map<String, dynamic> saveAdaptiveMemory(
  String path,
  Map<String, dynamic> memory,
  String key,
) =>
    _saveSessionEnvelope(path, memory, key);

/// Port of `load_adaptive_memory(path, key)`.
Map<String, dynamic> loadAdaptiveMemory(String path, String key) {
  if (!File(path).existsSync()) {
    return <String, dynamic>{
      'available': false,
      'memory': _emptyAdaptiveMemory(),
      'bounded': true,
    };
  }
  final decrypted = _loadSessionEnvelope(path, key);
  return <String, dynamic>{
    'available': true,
    'memory': decrypted['session'] ?? _emptyAdaptiveMemory(),
    'algorithm': 'kaalka',
    'bounded': true,
  };
}

Map<String, dynamic> _emptyAdaptiveMemory() => <String, dynamic>{
      'selectors': <String, dynamic>{},
      'healed_selectors': <String, dynamic>{},
      'pagination_patterns': <dynamic>[],
      'modal_solutions': <dynamic>[],
      'interaction_chains': <dynamic>[],
      'bounded': true,
    };

// ---------------------------------------------------------------------------
// core/distributed_extraction/distributed_checkpoint_engine.py
// ---------------------------------------------------------------------------

/// Port of `save_distributed_checkpoint(path, checkpoint, key)`.
Map<String, dynamic> saveDistributedCheckpoint(
  String path,
  Map<String, dynamic> checkpoint,
  String key,
) =>
    _saveSessionEnvelope(path, checkpoint, key);

/// Port of `load_distributed_checkpoint(path, key)`.
Map<String, dynamic> loadDistributedCheckpoint(String path, String key) {
  if (!File(path).existsSync()) {
    return <String, dynamic>{
      'available': false,
      'checkpoint': _emptyCheckpoint(),
      'bounded': true,
    };
  }
  final decrypted = _loadSessionEnvelope(path, key);
  return <String, dynamic>{
    'available': true,
    'checkpoint': decrypted['session'] ?? _emptyCheckpoint(),
    'algorithm': 'kaalka',
    'bounded': true,
  };
}

Map<String, dynamic> _emptyCheckpoint() => <String, dynamic>{
      'queue': <dynamic>[],
      'workers': <dynamic>[],
      'runtime_graph': <String, dynamic>{
        'nodes': <dynamic>[],
        'edges': <dynamic>[],
      },
      'identities': <dynamic>[],
      'adaptive_memory': <String, dynamic>{},
      'stream_runtime': <String, dynamic>{'events': <dynamic>[]},
      'tick': 0,
      'bounded': true,
    };

// ---------------------------------------------------------------------------
// core/connectors/live_runtime_memory_engine.py
// ---------------------------------------------------------------------------

/// Port of `save_live_runtime(path, memory, key)`.
Map<String, dynamic> saveLiveRuntime(
  String path,
  Map<String, dynamic> memory,
  String key,
) {
  final payload = _pyJsonSortKeys(memory);
  final encrypted = encryptValue(payload, key);
  final target = File(path);
  target.parent.createSync(recursive: true);
  final wrapper = <String, dynamic>{
    'encrypted': encrypted,
    'algorithm': 'kaalka',
  };
  target.writeAsStringSync(_pyJsonSortKeys(wrapper));
  return <String, dynamic>{
    'saved': true,
    'path': target.path,
    'algorithm': 'kaalka',
    'bounded': true,
  };
}

/// Port of `load_live_runtime(path, key)`.
Map<String, dynamic> loadLiveRuntime(String path, String key) {
  final target = File(path);
  if (!target.existsSync()) {
    return <String, dynamic>{
      'available': false,
      'memory': _emptyLiveMemory(),
      'bounded': true,
    };
  }

  final wrapper = jsonDecode(target.readAsStringSync()) as Map<String, dynamic>;
  // Python: json.loads(decrypt_value(wrapper["encrypted"])["decrypted"]).
  final decrypted = decryptValue(wrapper['encrypted'] as String, key);
  final memory = decrypted is Map
      ? Map<String, dynamic>.from(decrypted)
      : jsonDecode(decrypted as String) as Map<String, dynamic>;

  return <String, dynamic>{
    'available': true,
    'memory': memory,
    'algorithm': 'kaalka',
    'bounded': true,
  };
}

Map<String, dynamic> _emptyLiveMemory() => <String, dynamic>{
      'connector_states': <String, dynamic>{},
      'stream_states': <String, dynamic>{},
      'topology': <String, dynamic>{},
      'telemetry_lineage': <dynamic>[],
      'snapshots': <String, dynamic>{},
      'bounded': true,
    };

// ---------------------------------------------------------------------------
// core/auth/authentication_runtime_engine.py
// ---------------------------------------------------------------------------

/// Port of `authenticate_runtime(page, credentials, config)`.
///
/// The cookie/token/form injection side effects (inject_cookies /
/// inject_auth_tokens / page.fill+click) mutate a live Playwright page; the
/// RETURN VALUE is fully determined by [credentials] and [config] and is what
/// this port reproduces. Pass any non-null [page] to take the authenticated
/// branches (the form branch fires only when the page exposes fill+click).
Map<String, dynamic> authenticateRuntime(
  dynamic page,
  Map<String, dynamic> credentials,
  Map<String, dynamic> config,
) {
  final method = (config['method'] ?? 'cookie_injection').toString().trim();

  if (page == null) {
    return <String, dynamic>{
      'authenticated': false,
      'method': method,
      'reason': 'missing_page',
      'bounded': true,
    };
  }

  final hasFill = page is AuthPageStub ? page.hasFill : false;
  final hasClick = page is AuthPageStub ? page.hasClick : false;

  if (method == 'form_login') {
    if (hasFill && hasClick) {
      // Side effects only; no observable change to the return value.
    }
    return <String, dynamic>{
      'authenticated': true,
      'method': method,
      'bounded': true,
    };
  }

  if (method == 'cookie_injection') {
    final cookies = List<dynamic>.from(
        (credentials['cookies'] as List<dynamic>?) ?? <dynamic>[]);
    return <String, dynamic>{
      'authenticated': true,
      'method': method,
      'cookie_count': cookies.length,
      'bounded': true,
    };
  }

  if (method == 'token_injection') {
    final tokens = List<dynamic>.from(
        (credentials['tokens'] as List<dynamic>?) ?? <dynamic>[]);
    return <String, dynamic>{
      'authenticated': true,
      'method': method,
      'token_count': tokens.length,
      'bounded': true,
    };
  }

  if (method == 'persistent_auth_replay') {
    return <String, dynamic>{
      'authenticated': true,
      'method': method,
      'bounded': true,
    };
  }

  return <String, dynamic>{
    'authenticated': false,
    'method': method,
    'reason': 'unsupported_method',
    'bounded': true,
  };
}

/// Minimal stand-in for a Playwright page. A non-null page takes the
/// authenticated branches; [hasFill]/[hasClick] gate the form_login side
/// effects (which do not change the return value).
class AuthPageStub {
  AuthPageStub({this.hasFill = false, this.hasClick = false});
  final bool hasFill;
  final bool hasClick;
}
