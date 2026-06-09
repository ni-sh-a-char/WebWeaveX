import 'dart:convert';
import 'dart:io';

import 'package:test/test.dart';
import 'package:webweavex/src/adaptive/selector_healing.dart';
import 'package:webweavex/webweavex.dart' show computeDeterministicHash;

/// Cross-language parity for `heal_selector`, proven by deep-equality against
/// reference outputs captured from the canonical Python
/// `webweavex.heal_selector` (logic identical across 2.0.0/2.0.1 — verified by
/// `diff` of `core/adaptive/selector_healing_engine.py`). Deep-equality is a
/// stronger proof than hash equality and is independent of the Python hash fn.
void main() {
  group('heal_selector cross-language parity (deep-equality vs Python)', () {
    final vectorsFile =
        File('validation/parity/selector_healing_api_vectors.json');
    final vectors =
        (jsonDecode(vectorsFile.readAsStringSync()) as List<dynamic>)
            .map((e) => Map<String, dynamic>.from(e as Map))
            .toList();

    for (final v in vectors) {
      final id = v['id'] as String;
      final input = Map<String, dynamic>.from(v['input'] as Map);
      final expected = Map<String, dynamic>.from(v['expected'] as Map);

      test('[$id] Dart output deep-equals Python reference', () {
        final domNodes = (input['dom_nodes'] as List<dynamic>)
            .map((e) => Map<String, dynamic>.from(e as Map))
            .toList();
        final actual = healSelector(
          input['selector'] as String,
          domNodes,
          html: input['html'] as String,
        );

        // Strongest check: identical canonical hash ⟺ identical structure.
        expect(
          computeDeterministicHash(actual),
          equals(computeDeterministicHash(expected)),
          reason: 'hash mismatch for $id\nexpected=$expected\nactual=$actual',
        );
        // And an explicit field-level check for readability on failure.
        expect(actual['healed_selector'], equals(expected['healed_selector']));
        expect(actual['strategy'], equals(expected['strategy']));
        expect(actual['original'], equals(expected['original']));
        expect(actual['bounded'], isTrue);
      });
    }
  });

  group('heal_selector determinism + branch coverage', () {
    test('same input yields identical hash twice', () {
      final nodes = <Map<String, dynamic>>[
        <String, dynamic>{
          'tag': 'button',
          'text': 'Go',
          'attrs': <String, dynamic>{'id': 'g'}
        },
      ];
      final a = healSelector('#g', nodes);
      final b = healSelector('#g', nodes);
      expect(computeDeterministicHash(a), equals(computeDeterministicHash(b)));
    });

    test('empty dom + empty html -> structural_fallback div', () {
      final r = healSelector('.missing', <Map<String, dynamic>>[]);
      expect(r['strategy'], equals('structural_fallback'));
      expect(r['healed_selector'], equals('div'));
      expect(r['bounded'], isTrue);
    });

    test('buildSemanticAnchor sorts anchors and matches token', () {
      final a = buildSemanticAnchor(
        '#email',
        '<h2>Email Address</h2><label>Other</label>',
      );
      final anchors = a['anchors'] as List<dynamic>;
      expect(anchors.length, equals(2));
      // sorted by (type, text): h2 before label
      expect((anchors[0] as Map)['type'], equals('h2'));
      final matched = a['matched'] as List<dynamic>;
      expect(matched.length, equals(1));
      expect((matched[0] as Map)['text'], equals('Email Address'));
    });
  });
}
