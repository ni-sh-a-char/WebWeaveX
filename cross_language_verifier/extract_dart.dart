// Dart extraction runner over the torture set + corpus (same inputs as
// extract_py.py / extract_js.mjs). Run from repo root:
//   dart run cross_language_verifier/extract_dart.dart cross_language_verifier <out.json>
import 'dart:convert';
import 'dart:io';

import 'package:webweavex/src/crypto/hashing.dart';
import 'package:webweavex/src/crypto/utf8_parity.dart';
import 'package:webweavex/src/extraction/html_semantic_extraction.dart';

const Map<String, String> torture = {
  'unclosed': "<html><body><h1>Open heading<p>para<a href='/x'>link<div>tail",
  'nested_misnest': '<b><i>bold-italic</b></i><h2>after</h2>',
  'entities':
      '<title>A &amp; B &lt;C&gt; &#8212; &quot;D&quot; &copy;</title><h1>&nbsp;E&nbsp;</h1>',
  'comments_scripts':
      "<!-- c --><script>var x='<h1>not</h1>';</script><h1>real</h1><style>h2{}</style><a href='u'>l</a>",
  'attr_quirks':
      '<a href=unquoted>u</a><a href=\'single\'>s</a><a HREF="UPPER">c</a><a>none</a>',
  'tables_lists':
      '<table><tr><td>c1</td><td>c2</td></tr></table><ul><li>i1</li><li>i2</li></ul><ol><li>o1</li></ol>',
  'code_blocks': '<pre><code>if (a &lt; b) { run(); }</code></pre><p>after</p>',
  'metadata':
      '<head><title>T</title><meta name=\'description\' content=\'D\'><meta property=\'og:title\' content=\'OG\'>'
      '<script type=\'application/ld+json\'>{"@type":"Article"}</script></head><body><h1>B</h1></body>',
  'empty': '',
  'text_only': 'no tags at all, just text',
  'broken_brackets':
      "<h1>a < b</h1><a href='x'>y</a>< not-a-tag <h2>z</h2>",
  'duplicate_links':
      "<a href='/a'>1</a><a href='/a'>2</a><a href='/b'>3</a><a href='/a'>4</a>",
  'unicode_content':
      "<title>café 中文 🚀</title><h1>शीर्ष</h1><a href='/ü'>link</a>",
};

void main(List<String> argv) {
  final vdir = argv[0];
  final out = <String, dynamic>{
    'torture': <String, dynamic>{},
    'corpus': <String, dynamic>{},
  };
  final deepNesting = '${'<div>' * 50}<h3>deep</h3>${'</div>' * 50}';
  final allTorture = {...torture, 'deep_nesting': deepNesting};
  allTorture.forEach((tid, html) {
    final h = extractSemanticHtml(html);
    final c = extractSemanticContent(html);
    (out['torture'] as Map)[tid] = {
      'html_hash': computeDeterministicHash(h),
      'content_hash': computeDeterministicHash(c),
      'html_out': h,
      'content_out': c,
    };
  });
  final man = jsonDecode(
          File('$vdir/corpus/manifest.json').readAsStringSync())
      as List<dynamic>;
  for (final e in man) {
    final f = (e as Map)['file'] as String;
    final raw = File('$vdir/corpus/$f').readAsBytesSync();
    final text = utf8DecodeParity(raw, allowMalformed: true);
    final h = extractSemanticHtml(text);
    final c = extractSemanticContent(text);
    (out['corpus'] as Map)[f] = {
      'html_hash': computeDeterministicHash(h),
      'content_hash': computeDeterministicHash(c),
    };
  }
  File(argv[1]).writeAsStringSync(
      const JsonEncoder.withIndent(' ').convert(out));
  stdout.write('dart extraction: ${(out['torture'] as Map).length} torture + '
      '${(out['corpus'] as Map).length} corpus pages\n');
}
