import 'dart:convert';

/// Cross-language UTF-8 decode.
///
/// `dart:convert` strips a leading BOM (U+FEFF) when decoding, while Python
/// `bytes.decode('utf-8')` and Node `Buffer.toString('utf8')` preserve it.
/// Canonical behavior is preserve — payloads whose canonical form begins with
/// U+FEFF must round-trip byte-identically in every language.
final String _bom = String.fromCharCode(0xFEFF);

String utf8DecodeParity(List<int> bytes, {bool allowMalformed = false}) {
  final s = utf8.decode(bytes, allowMalformed: allowMalformed);
  if (bytes.length >= 3 &&
      bytes[0] == 0xEF &&
      bytes[1] == 0xBB &&
      bytes[2] == 0xBF &&
      !s.startsWith(_bom)) {
    return '$_bom$s';
  }
  return s;
}
