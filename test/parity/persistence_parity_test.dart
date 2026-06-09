import 'dart:convert';
import 'dart:io';

import 'package:test/test.dart';
import 'package:webweavex/src/persistence/persistence.dart';
import 'package:webweavex/webweavex.dart' show computeDeterministicHash;

dynamic _callApi(String api, Map<String, dynamic> input) {
  switch (api) {
    case 'fingerprint':
      final token = input['token'] as String?;
      final fp = token == null
          ? fingerprint(input['payload'])
          : fingerprint(input['payload'], token);
      // Python hashes the returned hex string; mirror that here.
      return fp;
    case 'encrypt_session_state':
      return encryptSessionState(
        Map<String, dynamic>.from(input['session'] as Map),
        input['key'] as String,
      );
    case 'decrypt_session_state':
      // Vector stores the plaintext session + key; encrypt then decrypt so the
      // ciphertext is reproduced deterministically before comparison.
      final encrypted = encryptSessionState(
        Map<String, dynamic>.from(input['session'] as Map),
        input['key'] as String,
      );
      return decryptSessionState(encrypted, input['key'] as String);
    case 'authenticate_runtime':
      final page = _pageFor(input['page']);
      return authenticateRuntime(
        page,
        Map<String, dynamic>.from(input['credentials'] as Map),
        Map<String, dynamic>.from(input['config'] as Map),
      );
    default:
      throw StateError('unknown api $api');
  }
}

dynamic _pageFor(dynamic spec) {
  if (spec == null) return null;
  if (spec == 'stub_form') {
    return AuthPageStub(hasFill: true, hasClick: true);
  }
  return AuthPageStub();
}

void main() {
  group('persistence API parity (Python det_hash gate)', () {
    final vectorsFile = File('validation/parity/persistence_api_vectors.json');
    final vectors =
        (jsonDecode(vectorsFile.readAsStringSync()) as List<dynamic>)
            .map((e) => Map<String, dynamic>.from(e as Map))
            .toList();

    for (var i = 0; i < vectors.length; i++) {
      final v = vectors[i];
      final api = v['api'] as String;
      final input = Map<String, dynamic>.from(v['input'] as Map);
      final expected = v['det_hash'] as String;

      test('[$i] $api -> $expected', () {
        final result = _callApi(api, input);
        final actual = computeDeterministicHash(result);
        expect(actual, equals(expected),
            reason: 'parity mismatch for $api with input $input');
      });
    }

    test('fingerprint raw hex matches Python byte cipher', () {
      final v = vectors.firstWhere((e) => e['raw'] != null);
      final out = fingerprint(
        (v['input'] as Map)['payload'],
        ((v['input'] as Map)['token']) as String,
      );
      expect(out, equals(v['raw']));
    });
  });

  group('save/load roundtrips (temp-file deep equality)', () {
    late Directory tempDir;
    const key = 'parity-roundtrip-key';

    setUp(() {
      tempDir = Directory.systemTemp.createTempSync('wwx_persist_');
    });
    tearDown(() {
      if (tempDir.existsSync()) tempDir.deleteSync(recursive: true);
    });

    String p(String name) => '${tempDir.path}${Platform.pathSeparator}$name';

    test('encrypted session save -> load deep-equals input', () {
      final session = <String, dynamic>{
        'cookies': <dynamic>[
          <String, dynamic>{'name': 'sid', 'value': 'abc'}
        ],
        'headers': <String, dynamic>{'User-Agent': 'wwx'},
        'auth_tokens': <dynamic>['t1'],
        'authenticated': true,
        'bounded': true,
      };
      final saved = saveEncryptedSession(p('s.json'), session, key);
      expect(saved['saved'], isTrue);
      expect(File(p('s.json')).existsSync(), isTrue);

      final loaded = loadEncryptedSession(p('s.json'), key);
      expect(loaded['available'], isTrue);
      expect(loaded['session'], equals(session));
    });

    test('load_encrypted_session missing path -> default empty session', () {
      final loaded = loadEncryptedSession(p('missing.json'), key);
      expect(loaded['available'], isFalse);
      final s = loaded['session'] as Map<String, dynamic>;
      expect(s['authenticated'], isFalse);
      expect(s['cookies'], equals(<dynamic>[]));
    });

    test('load_encrypted_session corrupt file -> available:false with reason',
        () {
      File(p('bad.json')).writeAsStringSync('{not valid json');
      final loaded = loadEncryptedSession(p('bad.json'), key);
      expect(loaded['available'], isFalse);
      expect(loaded.containsKey('reason'), isTrue);
    });

    test('browser identity save -> load deep-equals input', () {
      final identity = <String, dynamic>{
        'user_agent': 'Mozilla/5.0',
        'viewport': <String, dynamic>{'width': 1920, 'height': 1080},
        'locale': 'en-US',
        'bounded': true,
      };
      saveBrowserIdentity(p('id.json'), identity, key);
      final loaded = loadBrowserIdentity(p('id.json'), key);
      expect(loaded['available'], isTrue);
      expect(loaded['identity'], equals(identity));
    });

    test('load_browser_identity missing -> available:false empty identity', () {
      final loaded = loadBrowserIdentity(p('missing.json'), key);
      expect(loaded['available'], isFalse);
      expect(loaded['identity'], equals(<String, dynamic>{}));
    });

    test('adaptive memory save -> load deep-equals input', () {
      final memory = <String, dynamic>{
        'selectors': <String, dynamic>{'#title': 'h1'},
        'healed_selectors': <String, dynamic>{},
        'pagination_patterns': <dynamic>['next'],
        'modal_solutions': <dynamic>[],
        'interaction_chains': <dynamic>[],
        'bounded': true,
      };
      saveAdaptiveMemory(p('mem.json'), memory, key);
      final loaded = loadAdaptiveMemory(p('mem.json'), key);
      expect(loaded['available'], isTrue);
      expect(loaded['memory'], equals(memory));
    });

    test('load_adaptive_memory missing -> available:false empty memory', () {
      final loaded = loadAdaptiveMemory(p('missing.json'), key);
      expect(loaded['available'], isFalse);
      final m = loaded['memory'] as Map<String, dynamic>;
      expect(m['selectors'], equals(<String, dynamic>{}));
      expect(m['bounded'], isTrue);
    });

    test('distributed checkpoint save -> load deep-equals input', () {
      final checkpoint = <String, dynamic>{
        'queue': <dynamic>['u1', 'u2'],
        'workers': <dynamic>['w1'],
        'runtime_graph': <String, dynamic>{
          'nodes': <dynamic>[],
          'edges': <dynamic>[]
        },
        'identities': <dynamic>[],
        'adaptive_memory': <String, dynamic>{},
        'stream_runtime': <String, dynamic>{'events': <dynamic>[]},
        'tick': 7,
        'bounded': true,
      };
      saveDistributedCheckpoint(p('cp.json'), checkpoint, key);
      final loaded = loadDistributedCheckpoint(p('cp.json'), key);
      expect(loaded['available'], isTrue);
      expect(loaded['checkpoint'], equals(checkpoint));
    });

    test('load_distributed_checkpoint missing -> available:false empty', () {
      final loaded = loadDistributedCheckpoint(p('missing.json'), key);
      expect(loaded['available'], isFalse);
      final c = loaded['checkpoint'] as Map<String, dynamic>;
      expect(c['tick'], equals(0));
      expect(
          c['runtime_graph'],
          equals(
              <String, dynamic>{'nodes': <dynamic>[], 'edges': <dynamic>[]}));
    });

    test('live runtime save -> load deep-equals input', () {
      final memory = <String, dynamic>{
        'connector_states': <String, dynamic>{'pg': 'open'},
        'stream_states': <String, dynamic>{},
        'topology': <String, dynamic>{'nodes': 2},
        'telemetry_lineage': <dynamic>['e1'],
        'snapshots': <String, dynamic>{},
        'bounded': true,
      };
      saveLiveRuntime(p('live.json'), memory, key);
      final loaded = loadLiveRuntime(p('live.json'), key);
      expect(loaded['available'], isTrue);
      expect(loaded['memory'], equals(memory));
    });

    test('load_live_runtime missing -> available:false empty memory', () {
      final loaded = loadLiveRuntime(p('missing.json'), key);
      expect(loaded['available'], isFalse);
      final m = loaded['memory'] as Map<String, dynamic>;
      expect(m['connector_states'], equals(<String, dynamic>{}));
      expect(m['telemetry_lineage'], equals(<dynamic>[]));
    });
  });

  group('branch coverage', () {
    test('authenticate_runtime null page -> missing_page', () {
      final r = authenticateRuntime(null, <String, dynamic>{},
          <String, dynamic>{'method': 'cookie_injection'});
      expect(r['authenticated'], isFalse);
      expect(r['reason'], equals('missing_page'));
    });

    test('authenticate_runtime unsupported method', () {
      final r = authenticateRuntime(AuthPageStub(), <String, dynamic>{},
          <String, dynamic>{'method': 'nope'});
      expect(r['authenticated'], isFalse);
      expect(r['reason'], equals('unsupported_method'));
    });

    test('authenticate_runtime default method is cookie_injection', () {
      final r = authenticateRuntime(
          AuthPageStub(), <String, dynamic>{}, <String, dynamic>{});
      expect(r['method'], equals('cookie_injection'));
      expect(r['cookie_count'], equals(0));
    });

    test('authenticate_runtime form_login with fill+click', () {
      final r = authenticateRuntime(
        AuthPageStub(hasFill: true, hasClick: true),
        <String, dynamic>{'username': 'u', 'password': 'p'},
        <String, dynamic>{'method': 'form_login'},
      );
      expect(r['authenticated'], isTrue);
      expect(r['method'], equals('form_login'));
    });

    test('authenticate_runtime token_injection counts tokens', () {
      final r = authenticateRuntime(
        AuthPageStub(),
        <String, dynamic>{
          'tokens': <dynamic>[
            <String, dynamic>{'type': 'bearer', 'value': 'x'}
          ]
        },
        <String, dynamic>{'method': 'token_injection'},
      );
      expect(r['token_count'], equals(1));
    });

    test('authenticate_runtime persistent_auth_replay', () {
      final r = authenticateRuntime(
        AuthPageStub(),
        <String, dynamic>{
          'session': <String, dynamic>{
            'cookies': <dynamic>[],
            'auth_tokens': <dynamic>[]
          }
        },
        <String, dynamic>{'method': 'persistent_auth_replay'},
      );
      expect(r['authenticated'], isTrue);
      expect(r['method'], equals('persistent_auth_replay'));
    });

    test('fingerprint bytes payload path', () {
      final asString = fingerprint('abc', 'tok');
      final asBytes = fingerprint(utf8.encode('abc'), 'tok');
      expect(asBytes, equals(asString));
    });

    test('fingerprint default token', () {
      final out = fingerprint('x');
      expect(out, isNotEmpty);
    });

    test('encrypt -> decrypt session state in-memory roundtrip', () {
      final session = <String, dynamic>{
        'a': 1,
        'b': <dynamic>[1, 2, 3]
      };
      final enc = encryptSessionState(session, 'k');
      expect(enc['payload_type'], equals('session'));
      final dec = decryptSessionState(enc, 'k');
      expect(dec['session'], equals(session));
    });

    test('dumpsDeterministic sorts lists by canonical json', () {
      expect(dumpsDeterministic(<dynamic>[3, 1, 2]), equals('[1,2,3]'));
    });
  });
}
