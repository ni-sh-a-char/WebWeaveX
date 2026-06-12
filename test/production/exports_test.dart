import 'package:test/test.dart';
import 'package:webweavex/webweavex.dart' as wwx;

void main() {
  test('public exports', () {
    expect(wwx.extractWeb, isNotNull);
    expect(wwx.encryptValue, isNotNull);
    expect(wwx.validateReplayEquivalence, isNotNull);
    expect(wwx.version, '2.1.0');
  });
}
