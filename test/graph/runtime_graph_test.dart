import 'package:test/test.dart';
import 'package:webweavex/webweavex.dart';

void main() {
  test('buildRuntimeGraph is bounded', () {
    final g = buildRuntimeGraph({'nodes': <dynamic>[], 'edges': <dynamic>[]});
    expect(g.bounded, isTrue);
    expect(graphFingerprint(g), isNotEmpty);
  });
}
