/// Phase B port of core.ast.python_ast_engine.parse_python_ast (+ its private
/// `_node`). Like the JS branch's hand-written `src/ast/pythonAstEngine.ts`,
/// this is a lightweight line/indent scanner that reproduces the summary
/// CPython's `ast.walk` produces (imports / functions / classes / assignments
/// with line spans) — proven against executed CPython output by the
/// validation/semantic_ir/ harness.
library;

import 'py_compat.dart';

const String _ident = '[A-Za-z_][A-Za-z0-9_]*';

class _LogicalLine {
  _LogicalLine(this.text, this.lineno, this.endLineno, this.indent);
  final String text;
  final int lineno;
  final int endLineno;
  final int indent;
}

class _ScannedStmt {
  _ScannedStmt(this.kind, this.depth, this.lineno, this.endLineno, this.data);
  final String kind;
  final int depth;
  final int lineno;
  final int endLineno;
  final Map<String, dynamic> data;
}

Exception _syntaxError(int line) =>
    FormatException('invalid syntax (<unknown>, line $line)');

/// Python-validity gate: rejects lines that cannot begin a valid Python
/// logical line (CPython ast.parse raises on all of these). Extended
/// after real-world testing hit `/**`-led TypeScript sources that
/// CPython rejects but the original narrow gate accepted. `*` (starred
/// assignment), `.` (float literal), `+ - ~ @` (unary/decorator) remain
/// valid starters.
void _validateLine(String stripped, int lineno) {
  if (stripped.isEmpty) return;
  if (RegExp(r'^[<>%?\\/,;:=&|!)\]}]').hasMatch(stripped)) {
    throw _syntaxError(lineno);
  }
}

List<_LogicalLine> _logicalLines(String code) {
  final raw = code.split(RegExp(r'\r?\n'));
  final out = <_LogicalLine>[];
  var buf = '';
  var start = 0;
  var depth = 0;
  var indent = 0;
  String? inStr;
  for (var i = 0; i < raw.length; i++) {
    final line = raw[i];
    if (buf.isEmpty) {
      if (line.trim().isEmpty || line.trim().startsWith('#')) continue;
      start = i + 1;
      indent = RegExp(r'^[ \t]*')
          .firstMatch(line)![0]!
          .replaceAll('\t', '        ')
          .length;
    }
    buf += (buf.isNotEmpty ? '\n' : '') + line;
    // track bracket depth + triple strings (rough)
    var j = 0;
    while (j < line.length) {
      final ch = line[j];
      final three =
          line.substring(j, j + 3 > line.length ? line.length : j + 3);
      if (inStr != null) {
        if (three == inStr) {
          inStr = null;
          j += 3;
          continue;
        }
        j++;
        continue;
      }
      if (three == '"""' || three == "'''") {
        inStr = three;
        j += 3;
        continue;
      }
      if (ch == '#') break;
      if ('([{'.contains(ch)) {
        depth++;
      } else if (')]}'.contains(ch)) {
        depth--;
      }
      j++;
    }
    final endsContinuation = line.trimRight().endsWith(r'\');
    if (depth > 0 || inStr != null || endsContinuation) continue;
    out.add(_LogicalLine(buf, start, i + 1, indent));
    buf = '';
    depth = 0;
  }
  if (buf.isNotEmpty) out.add(_LogicalLine(buf, start, raw.length, indent));
  return out;
}

int _blockEnd(List<_LogicalLine> lines, int idx) {
  final base = lines[idx].indent;
  var end = lines[idx].endLineno;
  for (var j = idx + 1; j < lines.length; j++) {
    if (lines[j].indent <= base) break;
    end = lines[j].endLineno;
  }
  return end;
}

Map<String, dynamic> _node(_ScannedStmt s) => <String, dynamic>{
      'type': s.kind,
      'lineno': s.lineno,
      'end_lineno': s.endLineno,
    };

/// Port of core.ast.python_ast_engine.parse_python_ast.
Map<String, dynamic> parsePythonAst(String code) {
  final lines = _logicalLines(code);
  final stmts = <_ScannedStmt>[];

  for (var idx = 0; idx < lines.length; idx++) {
    final text = lines[idx].text;
    final lineno = lines[idx].lineno;
    final indent = lines[idx].indent;
    // collapse continuation/grouping newlines for statement matching
    final stripped = text
        .trim()
        .replaceAll(RegExp(r'\\\s*\n\s*'), ' ')
        .replaceAll(RegExp(r'\s*\n\s*'), ' ');
    final depth = indent ~/ 4;
    _validateLine(stripped.split('\n')[0], lineno);

    var m = RegExp(r'^import\s+(.+)$').firstMatch(stripped);
    if (m != null && !stripped.startsWith('import(')) {
      final modules = <String>[
        for (final s in m.group(1)!.split(','))
          if (s.trim().split(RegExp(r'\s+as\s+'))[0].trim().isNotEmpty)
            s.trim().split(RegExp(r'\s+as\s+'))[0].trim()
      ];
      stmts.add(_ScannedStmt('Import', depth, lineno, lines[idx].endLineno,
          <String, dynamic>{'modules': modules}));
      continue;
    }
    m = RegExp(r'^from\s+([.\w]+)\s+import\s+(.+)$').firstMatch(stripped);
    if (m != null) {
      final names = <String>[
        for (final s in m.group(2)!.replaceAll(RegExp(r'[()]'), '').split(','))
          if (s.trim().split(RegExp(r'\s+as\s+'))[0].trim().isNotEmpty)
            s.trim().split(RegExp(r'\s+as\s+'))[0].trim()
      ];
      stmts.add(_ScannedStmt(
          'ImportFrom', depth, lineno, lines[idx].endLineno, <String, dynamic>{
        'module': m.group(1),
        'names': names,
      }));
      continue;
    }
    // CPython's ast.walk collects ast.FunctionDef only; `async def` produces
    // ast.AsyncFunctionDef, which isinstance(node, ast.FunctionDef) does NOT
    // match — so async defs are intentionally not scanned (the JS branch's
    // scanner matches them; that is a JS-branch divergence from canonical
    // Python, documented in SEMANTIC_IR_PARITY_REPORT.md).
    m = RegExp('^def\\s+($_ident)\\s*\\(([\\s\\S]*?)\\)\\s*(?:->[^:]+)?:')
        .firstMatch(stripped);
    if (m != null) {
      final args = <String>[
        for (final s in m.group(2)!.split(','))
          if (s
                      .trim()
                      .split(RegExp(r'[:=]'))[0]
                      .trim()
                      .replaceFirst(RegExp(r'^\*+'), '') !=
                  '' &&
              s
                      .trim()
                      .split(RegExp(r'[:=]'))[0]
                      .trim()
                      .replaceFirst(RegExp(r'^\*+'), '') !=
                  '/')
            s
                .trim()
                .split(RegExp(r'[:=]'))[0]
                .trim()
                .replaceFirst(RegExp(r'^\*+'), '')
      ];
      stmts.add(_ScannedStmt('FunctionDef', depth, lineno,
          _blockEnd(lines, idx), <String, dynamic>{
        'name': m.group(1),
        'args': args,
      }));
      continue;
    }
    m = RegExp('^class\\s+($_ident)\\s*(?:\\(([^)]*)\\))?\\s*:')
        .firstMatch(stripped);
    if (m != null) {
      final bases = <dynamic>[
        for (final s in (m.group(2) ?? '').split(','))
          if (s.trim().isNotEmpty && !s.contains('='))
            RegExp('^$_ident\$').hasMatch(s.trim()) ? s.trim() : null
      ];
      stmts.add(_ScannedStmt('ClassDef', depth, lineno, _blockEnd(lines, idx),
          <String, dynamic>{'name': m.group(1), 'bases': bases}));
      continue;
    }
    m = RegExp('^((?:$_ident\\s*,\\s*)*$_ident)\\s*=(?!=)([\\s\\S]*)\$')
        .firstMatch(stripped);
    if (m != null &&
        !stripped.contains('==') &&
        !RegExp(r'^(if|while|for|return|yield|assert|del|import|from|pass|raise)\b')
            .hasMatch(stripped)) {
      final targets = <String>[
        for (final s in m.group(1)!.split(','))
          if (RegExp('^$_ident\$').hasMatch(s.trim())) s.trim()
      ];
      if (targets.isNotEmpty) {
        stmts.add(_ScannedStmt('Assign', depth, lineno, lines[idx].endLineno,
            <String, dynamic>{'targets': targets}));
      }
      continue;
    }
  }

  // ast.walk is breadth-first: order statements by nesting depth, then line
  final ordered = List<_ScannedStmt>.from(stmts)
    ..sort((a, b) {
      final d = a.depth - b.depth;
      return d != 0 ? d : a.lineno - b.lineno;
    });

  final imports = <Map<String, dynamic>>[];
  final functions = <Map<String, dynamic>>[];
  final classes = <Map<String, dynamic>>[];
  final assignments = <Map<String, dynamic>>[];
  for (final s in ordered) {
    if (s.kind == 'Import') {
      imports.add(
          <String, dynamic>{'modules': s.data['modules'], 'node': _node(s)});
    } else if (s.kind == 'ImportFrom') {
      imports.add(<String, dynamic>{
        'module': s.data['module'],
        'names': s.data['names'],
        'node': _node(s),
      });
    } else if (s.kind == 'FunctionDef') {
      functions.add(<String, dynamic>{
        'name': s.data['name'],
        'args': s.data['args'],
        'node': _node(s),
      });
    } else if (s.kind == 'ClassDef') {
      classes.add(<String, dynamic>{
        'name': s.data['name'],
        'bases': s.data['bases'],
        'node': _node(s),
      });
    } else {
      assignments.add(
          <String, dynamic>{'targets': s.data['targets'], 'node': _node(s)});
    }
  }

  return <String, dynamic>{
    'language': 'python',
    'imports': pyStableSortedBy(imports, (x) => pyToStr(x)),
    'functions': pyStableSortedBy(functions, (x) => x['name'] as String),
    'classes': pyStableSortedBy(classes, (x) => x['name'] as String),
    'assignments': assignments,
    'ast_grounded': true,
    'bounded': true,
  };
}
