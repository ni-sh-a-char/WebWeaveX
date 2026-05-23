import 'package:test/test.dart';
import 'package:webweavex/webweavex.dart';

void main() {
  test('runCanonicalPipeline text kind', () async {
    final out = await runCanonicalPipeline({
      'source': 'hello.txt',
      'sourceType': 'text',
    });
    expect(out['bounded'], isTrue);
    expect(out['ingestion'], isNotNull);
  });
}
