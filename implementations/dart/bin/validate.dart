import 'dart:convert';
import 'dart:io';
import 'package:collection/collection.dart';
import '../lib/webweavex.dart';
import '../lib/chunker.dart';
import '../lib/entities.dart';

void main() {
  const testCasesPath = '../../core/test_cases/test_cases.json';
  const outputDir = '../../test_output/dart';

  final testCasesFile = File(testCasesPath);
  if (!testCasesFile.existsSync()) {
    print('Test cases not found: $testCasesPath');
    exit(1);
  }

  final outputDirectory = Directory(outputDir);
  if (!outputDirectory.existsSync()) {
    outputDirectory.createSync(recursive: true);
  }

  final json = testCasesFile.readAsStringSync();
  final testCases = jsonDecode(json) as List<dynamic>;

  print('Exporting Dart outputs...');
  print('=' * 50);

  final testCaseNames = <String>[];

  final wx = WebWeaveX();

  for (final tc in testCases) {
    final name = (tc as Map<String, dynamic>)['name'] as String;
    final inputText = (tc['input'] as String?) ?? '';

    print('Processing: $name');

    final result = wx.extract(inputText);
    final outputPath = File('$outputDir/$name.json');
    outputPath.writeAsStringSync(
      const JsonEncoder.withIndent('  ').convert(result),
    );

    print('  Saved: ${outputPath.path}');
    testCaseNames.add(name);
  }

  print('=' * 50);
  print('Exported ${testCases.length} test cases to $outputDir');

  final manifestPath = File('$outputDir/manifest.json');
  manifestPath.writeAsStringSync(
    const JsonEncoder.withIndent(
      '  ',
    ).convert({'language': 'dart', 'test_cases': testCaseNames}),
  );
  print('Manifest: ${manifestPath.path}');
}
