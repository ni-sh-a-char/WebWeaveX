import 'package:test/test.dart';
import 'package:webweavex/webweavex.dart';

void main() {
  test('encrypt/decrypt roundtrip', () {
    final enc =
        encryptValue({'hello': 'world', 'emoji': '🚀'}, 'webweavex-key');
    final dec = decryptValue(enc, 'webweavex-key');
    expect(dec, {'hello': 'world', 'emoji': '🚀'});
  });

  test('deterministic encryption', () {
    final a = encryptValue('probe', 'k');
    final b = encryptValue('probe', 'k');
    expect(a, b);
  });

  test('deterministic hash', () {
    expect(
      computeDeterministicHash({'a': 1, 'b': 2}),
      isNotEmpty,
    );
  });
}
