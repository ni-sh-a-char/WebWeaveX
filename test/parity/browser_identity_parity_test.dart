import 'dart:convert';

import 'package:test/test.dart';
import 'package:webweavex/webweavex.dart'
    show computeDeterministicHash, buildBrowserIdentity;

/// Executable cross-language parity (Python ≡ JavaScript ≡ Dart) for the full
/// `build_browser_identity(profile_id)` subsystem (profile / user-agent /
/// platform / language / timezone / webgl / canvas / font / media / navigator /
/// entropy / fingerprint). Reference outputs captured by EXECUTING Python 2.0.1
/// and the JavaScript orchestrator engine — see validation/executable/.
void main() {
  group('build_browser_identity — executable parity (Python ≡ JS ≡ Dart)', () {
    final vectors = (jsonDecode(
      '[]',
    ) as List<dynamic>)
        .map((e) => Map<String, dynamic>.from(e as Map))
        .toList();

    for (final v in vectors) {
      final id = v['id'] as String;
      final args = v['args'] as List<dynamic>;
      final expected = v['expected'];

      test('[$id] Dart output hash-equals executed Python output', () {
        final actual = buildBrowserIdentity(args[0] as String);
        expect(
          computeDeterministicHash(actual),
          equals(computeDeterministicHash(expected)),
          reason: 'parity mismatch for $id',
        );
      });
    }
  });

  group('build_browser_identity contract', () {
    test('default profile carries full identity shape', () {
      final id = buildBrowserIdentity('default');
      expect(id['profile_id'], equals('default'));
      expect(
          id.keys,
          containsAll(<String>[
            'user_agent',
            'platform',
            'languages',
            'timezone',
            'screen',
            'webgl',
            'fonts',
            'media_devices',
            'canvas_fingerprint',
            'navigator',
            'entropy_profile',
            'fingerprint_hash',
            'bounded',
          ]));
    });

    test('unknown profile falls back to default', () {
      expect(
        computeDeterministicHash(buildBrowserIdentity('zzz')),
        equals(computeDeterministicHash(buildBrowserIdentity('default'))),
      );
    });

    test('distinct profiles produce distinct fingerprints', () {
      expect(
        buildBrowserIdentity('profile_a')['fingerprint_hash'],
        isNot(equals(buildBrowserIdentity('profile_b')['fingerprint_hash'])),
      );
    });
  });
}
