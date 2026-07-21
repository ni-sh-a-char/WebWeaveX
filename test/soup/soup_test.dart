import 'package:test/test.dart';
import 'package:webweavex/webweavex.dart';

void main() {
  group('soup HTML parser', () {
    test('Soup parses basic HTML', () {
      final soup = Soup('<html><body><h1>Hello</h1></body></html>');
      expect(soup, isNotNull);
    });

    test('htmlUnescape decodes entities', () {
      final result = htmlUnescape('&amp; &lt; &gt;');
      expect(result, equals('& < >'));
    });

    test('htmlUnescape handles numeric entities', () {
      final result = htmlUnescape('&#65; &#x41;');
      expect(result, equals('A A'));
    });

    test('htmlUnescape handles plain text', () {
      final result = htmlUnescape('hello world');
      expect(result, equals('hello world'));
    });
  });
}