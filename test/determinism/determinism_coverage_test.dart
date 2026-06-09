import 'package:test/test.dart';
import 'package:webweavex/src/determinism/dom_stabilization.dart';
import 'package:webweavex/src/determinism/fingerprint.dart';
import 'package:webweavex/src/determinism/normalization.dart';
import 'package:webweavex/src/determinism/stable_serialize.dart';
import 'package:webweavex/src/graph/runtime_graph.dart';

void main() {
  group('normalization_core normalizeRuntimeValueCore', () {
    test('CRLF and CR collapse to LF', () {
      expect(normalizeRuntimeValueCore('a\r\nb\rc'), 'a\nb\nc');
    });

    test('trailing whitespace stripped', () {
      expect(normalizeRuntimeValueCore('text   '), 'text');
      expect(normalizeRuntimeValueCore('line\t \n'), 'line');
    });

    test('empty string passes through', () {
      expect(normalizeRuntimeValueCore(''), '');
    });

    test('clean string unchanged', () {
      expect(normalizeRuntimeValueCore('clean'), 'clean');
    });
  });

  group('normalization_core stableSortKeys', () {
    test('sorts keys alphabetically', () {
      final out = stableSortKeys(<String, dynamic>{'b': 1, 'a': 2, 'c': 3});
      expect(out.keys.toList(), <String>['a', 'b', 'c']);
    });

    test('drops volatile keys', () {
      final out = stableSortKeys(<String, dynamic>{
        'keep': 1,
        'timestamp': 'x',
        'nonce': 'y',
        'uuid': 'z',
      });
      expect(out.containsKey('timestamp'), isFalse);
      expect(out.containsKey('nonce'), isFalse);
      expect(out.containsKey('uuid'), isFalse);
      expect(out['keep'], 1);
    });

    test('recurses into nested maps', () {
      final out = stableSortKeys(<String, dynamic>{
        'outer': <String, dynamic>{'z': 1, 'a': 2, 'nonce': 'drop'},
      });
      final inner = out['outer'] as Map<String, dynamic>;
      expect(inner.keys.toList(), <String>['a', 'z']);
      expect(inner.containsKey('nonce'), isFalse);
    });

    test('recurses into lists with map items and leaves scalars', () {
      final out = stableSortKeys(<String, dynamic>{
        'list': <dynamic>[
          <String, dynamic>{'b': 1, 'a': 2},
          5,
          'str',
        ],
      });
      final list = out['list'] as List<dynamic>;
      expect(
          (list[0] as Map<String, dynamic>).keys.toList(), <String>['a', 'b']);
      expect(list[1], 5);
      expect(list[2], 'str');
    });

    test('scalar values preserved (else branch)', () {
      final out =
          stableSortKeys(<String, dynamic>{'n': 42, 's': 'v', 'b': true});
      expect(out['n'], 42);
      expect(out['s'], 'v');
      expect(out['b'], true);
    });

    test('empty map yields empty map', () {
      expect(stableSortKeys(<String, dynamic>{}), <String, dynamic>{});
    });
  });

  group('normalization_core normalizeRuntimeState', () {
    test('delegates to stableSortKeys', () {
      final out = normalizeRuntimeState(<String, dynamic>{'b': 1, 'a': 2});
      expect((out as Map<String, dynamic>).keys.toList(), <String>['a', 'b']);
    });
  });

  group('normalization_core volatileRuntimeKeys', () {
    test('contains expected volatile keys', () {
      expect(volatileRuntimeKeys, contains('timestamp'));
      expect(volatileRuntimeKeys, contains('request_id'));
      expect(volatileRuntimeKeys, contains('csrf'));
      expect(volatileRuntimeKeys.contains('keep'), isFalse);
    });
  });

  group('normalization normalizeRuntimeValue', () {
    test('is deterministic', () {
      expect(normalizeRuntimeValue('café'), normalizeRuntimeValue('café'));
    });

    test('applies CRLF/trailing normalization', () {
      expect(normalizeRuntimeValue('a\r\nb   '), 'a\nb');
    });

    test('NFKC: composed and decomposed forms normalize equal', () {
      // U+00E9 (é) vs e + U+0301 (combining acute). NFKC makes them equal.
      const composed = 'café';
      const decomposed = 'café';
      final a = normalizeRuntimeValue(composed);
      final b = normalizeRuntimeValue(decomposed);
      expect(a, b);
    });

    test('NFKC: compatibility ligature/fullwidth folding', () {
      // Fullwidth 'Ａ' (U+FF21) folds to ASCII 'A' under NFKC.
      final out = normalizeRuntimeValue('Ａ');
      expect(out, 'A');
    });

    test('empty string normalizes to empty', () {
      expect(normalizeRuntimeValue(''), '');
    });

    test('plain ascii unchanged', () {
      expect(normalizeRuntimeValue('plain'), 'plain');
    });
  });

  group('stable_serialize stableSerialize', () {
    test('String branch goes through normalization', () {
      expect(stableSerialize('a\r\nb   '), 'a\nb');
    });

    test('Map branch sorts keys deterministically', () {
      final a = stableSerialize(<String, dynamic>{'b': 1, 'a': 2});
      final b = stableSerialize(<String, dynamic>{'a': 2, 'b': 1});
      expect(a, b);
      expect(a, '{"a":2,"b":1}');
    });

    test('Map branch drops volatile keys', () {
      final s = stableSerialize(<String, dynamic>{'a': 1, 'nonce': 'x'});
      expect(s, '{"a":1}');
    });

    test('List branch with map items maps to indexed keys', () {
      final s = stableSerialize(<dynamic>[
        <String, dynamic>{'b': 1, 'a': 2},
        99,
      ]);
      expect(s, '{"0":{"a":2,"b":1},"1":99}');
    });

    test('List branch with only scalars', () {
      final s = stableSerialize(<dynamic>[10, 'x', true]);
      expect(s, '{"0":10,"1":"x","2":true}');
    });

    test('RuntimeGraph branch', () {
      final g = RuntimeGraph(
        nodes: <RuntimeNode>[RuntimeNode(id: 'n1', type: 't')],
        edges: <RuntimeEdge>[],
      );
      final s = stableSerialize(g);
      expect(s, contains('"nodes"'));
      expect(s, contains('"bounded":true'));
    });

    test('fallthrough branch for scalars (int/null/bool)', () {
      expect(stableSerialize(5), '5');
      expect(stableSerialize(null), 'null');
      expect(stableSerialize(true), 'true');
    });

    test('empty map and empty list', () {
      expect(stableSerialize(<String, dynamic>{}), '{}');
      expect(stableSerialize(<dynamic>[]), '{}');
    });

    test('is deterministic across two calls', () {
      final v = <String, dynamic>{
        'z': <dynamic>[1, 2],
        'a': <String, dynamic>{'k': 'v'},
      };
      expect(stableSerialize(v), stableSerialize(v));
    });
  });

  group('dom_stabilization stabilizeDomHtml', () {
    test('stabilizes uuids', () {
      final out =
          stabilizeDomHtml('id=123e4567-e89b-12d3-a456-426614174000 end');
      expect(out, contains('uuid-stabilized'));
      expect(out, isNot(contains('123e4567')));
    });

    test('stabilizes ISO timestamps', () {
      final out = stabilizeDomHtml('at 2024-01-02T03:04:05.123Z done');
      expect(out, contains('timestamp-stabilized'));
    });

    test('strips react/vue/angular/nonce attributes', () {
      final html = '<div data-reactid="2" data-v-abc123="" '
          'ng-version="17.0.0" nonce="xyz">x</div>';
      final out = stabilizeDomHtml(html);
      expect(out, isNot(contains('data-react')));
      expect(out, isNot(contains('data-v-')));
      expect(out, isNot(contains('ng-version')));
      expect(out, isNot(contains('nonce=')));
    });

    test('replaces script bodies', () {
      final out = stabilizeDomHtml('<script>var x = Math.random();</script>');
      expect(out, '<script>stabilized</script>');
    });

    test('strips html comments', () {
      final out = stabilizeDomHtml('a<!-- comment -->b');
      expect(out, 'ab');
    });

    test('collapses whitespace and trims', () {
      final out = stabilizeDomHtml('   a    b   ');
      expect(out, 'a b');
    });

    test('empty input yields empty', () {
      expect(stabilizeDomHtml(''), '');
    });

    test('is deterministic for volatile html', () {
      const html = '<div nonce="r1" data-reactid="9">'
          '2024-05-05T01:02:03Z 11111111-2222-4333-8444-555555555555</div>'
          '<script>random()</script>';
      expect(stabilizeDomHtml(html), stabilizeDomHtml(html));
    });
  });

  group('dom_stabilization hashes', () {
    test('computeStableDomHash is 64-hex and deterministic', () {
      final h = computeStableDomHash('<div nonce="a">x</div>');
      expect(h, matches(RegExp(r'^[0-9a-f]{64}$')));
      expect(h, computeStableDomHash('<div nonce="b">x</div>'));
    });

    test('computeSpaFingerprint equals computeStableDomHash', () {
      const html = '<div>hello</div>';
      expect(computeSpaFingerprint(html), computeStableDomHash(html));
    });

    test('different stable content -> different hash', () {
      expect(
        computeStableDomHash('<div>a</div>'),
        isNot(computeStableDomHash('<div>b</div>')),
      );
    });
  });

  group('fingerprint computeGlobalRuntimeFingerprint', () {
    final graph = RuntimeGraph(
      nodes: <RuntimeNode>[RuntimeNode(id: 'n1', type: 'page')],
      edges: <RuntimeEdge>[],
    );

    test('deterministic for same envelope+graph', () {
      final env = <String, dynamic>{'pipeline_hash': 'abc', 'bounded': true};
      expect(
        computeGlobalRuntimeFingerprint(env, graph),
        computeGlobalRuntimeFingerprint(env, graph),
      );
    });

    test('bounded defaults to true when missing (?? branch)', () {
      final withBounded = <String, dynamic>{'pipeline_hash': 'p'};
      final withExplicit = <String, dynamic>{
        'pipeline_hash': 'p',
        'bounded': true,
      };
      expect(
        computeGlobalRuntimeFingerprint(withBounded, graph),
        computeGlobalRuntimeFingerprint(withExplicit, graph),
      );
    });

    test('explicit bounded false differs from default true', () {
      final f = <String, dynamic>{'pipeline_hash': 'p', 'bounded': false};
      final t = <String, dynamic>{'pipeline_hash': 'p', 'bounded': true};
      expect(
        computeGlobalRuntimeFingerprint(f, graph),
        isNot(computeGlobalRuntimeFingerprint(t, graph)),
      );
    });

    test('different pipeline_hash -> different fingerprint', () {
      final a = <String, dynamic>{'pipeline_hash': 'a'};
      final b = <String, dynamic>{'pipeline_hash': 'b'};
      expect(
        computeGlobalRuntimeFingerprint(a, graph),
        isNot(computeGlobalRuntimeFingerprint(b, graph)),
      );
    });

    test('produces a 64-char hex sha256 string', () {
      final env = <String, dynamic>{'pipeline_hash': 'h'};
      expect(
        computeGlobalRuntimeFingerprint(env, graph),
        matches(RegExp(r'^[0-9a-f]{64}$')),
      );
    });
  });
}
