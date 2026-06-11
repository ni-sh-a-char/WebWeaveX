import 'dart:convert';
import 'dart:io';

import 'package:webweavex/src/crypto/hashing.dart';
import 'package:webweavex/src/extraction/html_semantic_extraction.dart';

void main(List<String> argv) {
  final vectors = jsonDecode(File(argv[0]).readAsStringSync())
      as Map<String, dynamic>;
  final out = <String, dynamic>{};
  vectors.forEach((vid, html) {
    out[vid] = {
      'h': computeDeterministicHash(extractSemanticHtml(html as String)),
      'c': computeDeterministicHash(extractSemanticContent(html)),
    };
  });
  File(argv[1]).writeAsStringSync(jsonEncode(out));
  stdout.write('dart synth: ${out.length}\n');
}
