import 'package:webweavex/webweavex.dart';

void main() {
  const s = 'café\r\n日本語 🚀';
  print(stableSerialize(s));
  print(computeDeterministicHash(s));
}
