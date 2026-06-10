// Execute Dart semantic-IR ported functions; emit output + hash.
//   dart run validation/semantic_ir/run_dart.dart validation/semantic_ir/fixtures.json
import 'dart:convert';
import 'dart:io';

import 'package:webweavex/src/crypto/hashing.dart'
    show computeDeterministicHash;
import 'package:webweavex/src/semantic_ir/document_parser.dart';

List<Map<String, dynamic>> _claims(dynamic v) => <Map<String, dynamic>>[
      for (final e in v as List) Map<String, dynamic>.from(e as Map)
    ];

dynamic _call(String fn, List<dynamic> args) {
  switch (fn) {
    case 'extract_rhetorical_structure':
      return extractRhetoricalStructure(args[0] as String?);
    case 'assign_semantic_roles':
      return assignSemanticRoles(args[0] as String?);
    case 'extract_headings':
      return extractHeadings(args[0] as String?);
    case 'reconstruct_argument_dependencies':
      return reconstructArgumentDependencies(_claims(args[0]));
    case 'resolve_coreferences':
      return resolveCoreferences(args[0] as String?);
    default:
      throw StateError('unknown fn $fn');
  }
}

void main(List<String> argv) {
  final fixtures =
      jsonDecode(File(argv[0]).readAsStringSync()) as List<dynamic>;
  final out = <Map<String, dynamic>>[];
  for (final f in fixtures) {
    final fx = Map<String, dynamic>.from(f as Map);
    final fn = fx['fn'] as String;
    try {
      final result = _call(fn, fx['args'] as List<dynamic>);
      out.add(<String, dynamic>{
        'id': fx['id'],
        'fn': fn,
        'output': result,
        'hash': computeDeterministicHash(result),
      });
    } catch (e) {
      out.add(
          <String, dynamic>{'id': fx['id'], 'fn': fn, 'error': e.toString()});
    }
  }
  stdout.write(jsonEncode(out));
}
