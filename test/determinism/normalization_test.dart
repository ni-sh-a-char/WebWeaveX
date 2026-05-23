import 'package:test/test.dart';
import 'package:webweavex/webweavex.dart';

void main() {
  test('strips volatile keys', () {
    final s = stableSerialize({'z': 1, 'timestamp': 9, 'a': 2});
    expect(s.contains('timestamp'), isFalse);
    expect(s, '{"a":2,"z":1}');
  });

  test('normalizes CRLF', () {
    expect(stableSerialize('a\r\nb'), 'a\nb');
  });
}
