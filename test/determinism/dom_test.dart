import 'package:test/test.dart';
import 'package:webweavex/webweavex.dart';

void main() {
  test('stable dom hash', () {
    const html = '<div id="x">Hi</div>';
    expect(computeStableDomHash(html), computeStableDomHash(html));
  });
}
