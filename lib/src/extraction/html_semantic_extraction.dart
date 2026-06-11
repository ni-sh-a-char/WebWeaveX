/// Dart port of core/browser/html_semantic_extraction_engine.py and
/// core/extraction/semantic_content_extraction_engine.py — byte parity with
/// Python (bs4 html.parser) and JavaScript (PySoup), both certified on 130
/// real internet pages.
library;

import '../soup/soup.dart';

const int _maxLinks = 10000;

/// Port of `extract_semantic_html(html)`.
Map<String, dynamic> extractSemanticHtml(String html) {
  final soup = Soup(html);

  var title = '';
  final titleTag = soup.title;
  if (titleTag != null) {
    title = pyStrip(titleTag.text);
  }

  final links = <String>[];
  for (final link in soup.findAll('a', limit: _maxLinks)) {
    final href = link.get('href');
    if (href != null && href.isNotEmpty) {
      links.add(pyTruncate(href, 2000));
    }
  }

  final headings = <Map<String, dynamic>>[];
  for (final tag in ['h1', 'h2', 'h3']) {
    for (final node in soup.findAll(tag)) {
      headings.add({
        'tag': tag,
        'text': pyTruncate(node.getText(strip: true), 5000),
      });
    }
  }

  return {
    'title': title,
    'links': sortedSet(links),
    'headings': headings,
    'text': pyTruncate(soup.getText(sep: '\n'), 5000000),
    'bounded': true,
  };
}

/// Port of `extract_semantic_content(html)`.
Map<String, dynamic> extractSemanticContent(String html) {
  final soup = Soup(html);

  final headings = <Map<String, dynamic>>[];
  for (final level in ['h1', 'h2', 'h3']) {
    for (final node in soup.findAll(level)) {
      headings.add({
        'level': level,
        'text': pyTruncate(node.getText(strip: true), 5000),
      });
    }
  }

  final paragraphs = <String>[];
  for (final p in soup.findAll('p')) {
    final text = p.getText(strip: true);
    if (text.isNotEmpty) {
      paragraphs.add(pyTruncate(text, 10000));
    }
  }

  final links = <String>[];
  for (final a in soup.findAll('a', limit: _maxLinks)) {
    final href = a.get('href');
    if (href != null && href.isNotEmpty) {
      links.add(pyTruncate(href, 2000));
    }
  }

  return {
    'headings': headings,
    'paragraphs': paragraphs,
    'links': sortedSet(links),
    'bounded': true,
  };
}
