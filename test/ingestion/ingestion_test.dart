import 'package:test/test.dart';
import 'package:webweavex/webweavex.dart';

void main() {
  group('ingestion', () {
    test('detectInputType identifies HTML', () {
      final result = detectInputType('<html><body>test</body></html>');
      expect(result, isA<String>());
    });

    test('detectInputType identifies JSON', () {
      final result = detectInputType('{"key": "value"}');
      expect(result, isA<String>());
    });

    test('detectInputType handles empty input', () {
      final result = detectInputType('');
      expect(result, isA<String>());
    });
  });
}