import 'dart:convert';
import 'dart:io';

import 'package:test/test.dart';
import 'package:webweavex/src/interaction/interaction_replay.dart';
import 'package:webweavex/webweavex.dart' show computeDeterministicHash;

/// Cross-language parity for `replay_interactions`, proven by deep-equality
/// against reference outputs captured from the canonical Python 2.0.1
/// `webweavex.replay_interactions(None, log)`. The returned structure is a pure
/// function of the interaction log; the live-page dispatch is the bounded edge.
void main() {
  group('replay_interactions cross-language parity (vs Python 2.0.1)', () {
    final vectorsFile =
        File('validation/parity/interaction_replay_api_vectors.json');
    final vectors =
        (jsonDecode(vectorsFile.readAsStringSync()) as List<dynamic>)
            .map((e) => Map<String, dynamic>.from(e as Map))
            .toList();

    for (final v in vectors) {
      final id = v['id'] as String;
      final input = Map<String, dynamic>.from(v['input'] as Map);
      final expected = Map<String, dynamic>.from(v['expected'] as Map);

      test('[$id] Dart output deep-equals Python reference', () {
        final log = (input['interaction_log'] as List<dynamic>)
            .map((e) => Map<String, dynamic>.from(e as Map))
            .toList();
        final actual = replayInteractions(log);
        expect(
          computeDeterministicHash(actual),
          equals(computeDeterministicHash(expected)),
          reason: 'parity mismatch for $id\nexpected=$expected\nactual=$actual',
        );
        expect(actual['bounded'], isTrue);
      });
    }
  });

  group('replay_interactions branch coverage', () {
    test('page argument is accepted and ignored (output unchanged)', () {
      final log = <Map<String, dynamic>>[
        <String, dynamic>{'action': 'click', 'selector': '#a'},
      ];
      final withoutPage = replayInteractions(log);
      final withPage = replayInteractions(log, page: Object());
      expect(
        computeDeterministicHash(withoutPage),
        equals(computeDeterministicHash(withPage)),
      );
    });

    test('record_interaction trims and defaults', () {
      final r = recordInteraction('  tap  ', '  #x  ', step: 3);
      expect(r['id'], equals('interaction_3'));
      expect(r['timestamp'], equals(3));
      expect(r['action'], equals('tap'));
      expect(r['selector'], equals('#x'));
      expect(r['metadata'], equals(<String, dynamic>{}));
      expect(r['bounded'], isTrue);
    });

    test('replay is bounded at 1000 actions', () {
      final log = List<Map<String, dynamic>>.generate(
        1200,
        (i) => <String, dynamic>{'action': 'click', 'selector': '#$i'},
      );
      final r = replayInteractions(log);
      expect((r['replay'] as List).length, equals(1000));
    });
  });
}
