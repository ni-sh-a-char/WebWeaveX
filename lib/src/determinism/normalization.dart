import 'package:unorm_dart/unorm_dart.dart' as unorm;

import 'normalization_core.dart';

export 'normalization_core.dart';

/// NFKC + CRLF + trailing-whitespace normalization.
///
/// Order matches Python `normalize_runtime_value` (core/determinism/
/// normalization.py): NFKC first, then CRLF→LF, then trailing `\s+$` strip.
/// NFKC is pure Dart (`package:unorm_dart`) — byte-verified against
/// Python `unicodedata.normalize('NFKC')` and JavaScript
/// `String.normalize('NFKC')`.
String normalizeRuntimeValue(String value) =>
    normalizeRuntimeValueCore(unorm.nfkc(value));
