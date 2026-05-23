import 'package:webweavex/webweavex.dart';

void main() {
  const payload = {'hello': 'world', 'emoji': '🚀'};
  final enc = encryptValue(payload, 'parity-key');
  final dec = decryptValue(enc, 'parity-key');
  print('hash: ${computeDeterministicHash(payload)}');
  print('roundtrip: $dec');
}
