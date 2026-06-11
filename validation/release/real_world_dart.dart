// Real-world scenario runner (Dart) — mirror of real_world_py.py.
//   dart run validation/release/real_world_dart.dart <dart_clone> <js_clone>
import 'dart:convert';
import 'dart:io';

import 'package:webweavex/webweavex.dart';

String readF(String p) => File(p).readAsStringSync();

void main(List<String> argv) {
  final dart = argv[0];
  final js = argv[1];
  final readme = readF('$dart/README.md');
  final tsSrc = readF('$js/src/parsers/parserRegistry.ts');
  final page = readF('$dart/cross_language_verifier/corpus/page_0000.html');

  String h(dynamic v) => computeDeterministicHash(v);
  // code-point cap (Python slice semantics; UTF-16 substring diverges)
  String cap(String s, int n) => String.fromCharCodes(s.runes.take(n));

  final out = <String, String>{
    'doc_readme': h(compileDocument(cap(readme, 20000))),
    'query_doc_readme': h(queryDocuments(text: cap(readme, 20000))),
    'repo_ts_engine': h(compileRepository(tsSrc,
        path: 'src/parsers/parserRegistry.ts')),
    'query_repo_ts': h(queryRepository(
        source: tsSrc, path: 'src/parsers/parserRegistry.ts')),
    'reason_discourse':
        h(reasonSemantically('discourse', {'text': cap(readme, 5000)})),
    'reason_runtime': h(reasonSemantically('runtime',
        {'source': tsSrc, 'path': 'src/parsers/parserRegistry.ts'})),
    'app_cognition_real_page':
        h(runApplicationCognition('https://release.test/app', page)),
    'semantics_repo':
        h(querySemantics('repository', {'source': tsSrc, 'path': 'x.ts'})),
  };
  stdout.write(jsonEncode(out));
}
