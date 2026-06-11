/// Port of core/ingestion/universal_ingestion_engine.py: detect_input_type
/// and ingest_input.
library;

import 'package:webweavex/src/multimodal/universal_multimodal_extraction_engine.dart';

const Map<String, String> supportedExtensions = <String, String>{
  '.pdf': 'pdf',
  '.docx': 'docx',
  '.pptx': 'pptx',
  '.xlsx': 'xlsx',
  '.csv': 'csv',
  '.json': 'json',
  '.xml': 'xml',
  '.html': 'html',
  '.md': 'markdown',
  '.txt': 'text',
  '.py': 'repository',
  '.js': 'repository',
  '.ts': 'repository',
  '.zip': 'archive',
  '.png': 'image',
  '.jpg': 'image',
  '.jpeg': 'image',
};

/// Python `pathlib.Path(path).suffix`: the extension (including the dot) of
/// the final path component. Both `/` and `\` are treated as separators
/// (WindowsPath semantics; POSIX paths containing no backslashes behave
/// identically), trailing separators are ignored, and names whose only dot
/// is leading (".bashrc") or trailing ("file.") have no suffix.
String _pathSuffix(String path) {
  String trimmed = path;
  int end = trimmed.length;
  while (end > 0 &&
      (trimmed.codeUnitAt(end - 1) == 0x2F /* / */ ||
          trimmed.codeUnitAt(end - 1) == 0x5C /* \ */)) {
    end--;
  }
  trimmed = trimmed.substring(0, end);

  final int slash = trimmed.lastIndexOf('/');
  final int backslash = trimmed.lastIndexOf('\\');
  final int sep = slash > backslash ? slash : backslash;
  final String name = sep >= 0 ? trimmed.substring(sep + 1) : trimmed;

  final int dot = name.lastIndexOf('.');
  if (dot > 0 && dot < name.length - 1) {
    return name.substring(dot);
  }
  return '';
}

/// Port of universal_ingestion_engine.detect_input_type.
String detectInputType(String path) {
  if (path.startsWith('http://') || path.startsWith('https://')) {
    return 'url';
  }
  final String ext = _pathSuffix(path).toLowerCase();
  return supportedExtensions.containsKey(ext)
      ? supportedExtensions[ext]!
      : 'unknown';
}

/// Port of universal_ingestion_engine.ingest_input.
Map<String, dynamic> ingestInput(String path) {
  final String inputType = detectInputType(path);

  if (inputType == 'image') {
    final Map<String, dynamic> multimodal = extractMultimodal(path);

    return <String, dynamic>{
      'path': path,
      'type': 'image',
      'input_type': inputType,
      'supported': true,
      'multimodal': multimodal,
      'bounded': true,
    };
  }

  return <String, dynamic>{
    'path': path,
    'input_type': inputType,
    'supported': inputType != 'unknown',
    'bounded': true,
  };
}
