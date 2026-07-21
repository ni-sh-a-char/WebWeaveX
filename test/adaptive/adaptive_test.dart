import 'package:test/test.dart';
import 'package:webweavex/webweavex.dart';

void main() {
  group('adaptive - selector healing', () {
    test('healSelector returns candidates for broken selector', () {
      final domNodes = <Map<String, dynamic>>[
        {'tag': 'div', 'class': 'container', 'text': 'hello'},
      ];
      final result = healSelector('.broken', domNodes,
          html: '<div class="container">hello</div>');
      expect(result, isA<Map<String, dynamic>>());
      expect(result.containsKey('bounded'), isTrue);
      expect(result.containsKey('candidates'), isTrue);
      expect(result['bounded'], isTrue);
    });

    test('buildSemanticAnchor creates anchor from selector and html', () {
      final result = buildSemanticAnchor(
          '.test-class', '<div class="test-class">hello</div>');
      expect(result, isA<Map<String, dynamic>>());
    });
  });

  group('adaptive - modal recovery', () {
    test('recoverModalRuntime handles null page', () {
      final result = recoverModalRuntime(null);
      expect(result, isA<Map<String, dynamic>>());
    });

    test('recoverModalRuntime handles empty page', () {
      final result = recoverModalRuntime({});
      expect(result, isA<Map<String, dynamic>>());
    });
  });
}
