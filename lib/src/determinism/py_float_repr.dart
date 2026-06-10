/// Python `repr(float)` for doubles — the cross-language canonical float form.
///
/// Python (the reference runtime) renders shortest round-trip digits,
/// positional for decimal exponents in [-4, 15], otherwise scientific
/// notation with a sign and at-least-two-digit exponent. Dart's
/// `double.toString()` uses different thresholds (1e21 / 1e-6), so it cannot
/// be used for canonical serialization.
String pyFloatRepr(double x) {
  if (x.isNaN) return 'nan';
  if (x == double.infinity) return 'inf';
  if (x == double.negativeInfinity) return '-inf';
  if (x == x.truncateToDouble() && x.abs() < 1e16) {
    return x.toStringAsFixed(1);
  }
  final m = RegExp(r'^(-?)(\d)(?:\.(\d+))?e([+-])(\d+)$')
      .firstMatch(x.toStringAsExponential())!;
  final sign = m.group(1)!;
  final lead = m.group(2)!;
  final rest = m.group(3) ?? '';
  final esign = m.group(4)!;
  final eabs = int.parse(m.group(5)!);
  final exp = esign == '-' ? -eabs : eabs;
  if (exp < -4 || exp >= 16) {
    final mant = rest.isNotEmpty ? '$lead.$rest' : lead;
    return '$sign${mant}e$esign${eabs.toString().padLeft(2, '0')}';
  }
  final digits = lead + rest;
  if (exp < 0) {
    return '${sign}0.${'0' * (-exp - 1)}$digits';
  }
  if (digits.length <= exp + 1) {
    return '$sign${digits.padRight(exp + 1, '0')}.0';
  }
  return '$sign${digits.substring(0, exp + 1)}.${digits.substring(exp + 1)}';
}
