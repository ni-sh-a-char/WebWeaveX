import '../crypto/hashing.dart' show computeDeterministicHash;

final _uuidRe = RegExp(
  r'[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}',
  caseSensitive: false,
);
final _timestampRe = RegExp(
  r'\b\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:?\d{2})?\b',
);
final _reactRe = RegExp(r'data-react[a-z0-9-]*="[^"]*"', caseSensitive: false);
final _vueRe = RegExp(r'data-v-[a-z0-9]+="[^"]*"', caseSensitive: false);
final _angularRe = RegExp(
  r'\s(?:ng-version|_ngcontent[a-z0-9-]*|_nghost[a-z0-9-]*)="[^"]*"',
  caseSensitive: false,
);
final _nonceRe = RegExp(r'\snonce="[^"]*"', caseSensitive: false);
final _scriptBodyRe =
    RegExp(r'<script\b[^>]*>[\s\S]*?</script>', caseSensitive: false);

String stabilizeDomHtml(String html) {
  var s = html;
  s = s.replaceAll(_uuidRe, 'uuid-stabilized');
  s = s.replaceAll(_timestampRe, 'timestamp-stabilized');
  s = s.replaceAll(_reactRe, '');
  s = s.replaceAll(_vueRe, '');
  s = s.replaceAll(_angularRe, '');
  s = s.replaceAll(_nonceRe, '');
  s = s.replaceAll(_scriptBodyRe, '<script>stabilized</script>');
  s = s.replaceAll(RegExp(r'<!--[\s\S]*?-->'), '');
  s = s.replaceAll(RegExp(r'\s+'), ' ').trim();
  return s;
}

String computeStableDomHash(String html) =>
    computeDeterministicHash(stabilizeDomHtml(html));

String computeSpaFingerprint(String html) => computeStableDomHash(html);
