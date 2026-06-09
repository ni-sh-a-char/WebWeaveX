/// Deterministic selector-healing runtime, ported from the canonical Python
/// `core.adaptive.selector_healing_engine` (+ `semantic_anchor_engine`).
///
/// Parity scope:
///   * The DOM-node strategies (`text_anchor`, `attribute_anchor`,
///     `structural_fallback`) are a full-fidelity port — pure functions over the
///     caller-supplied `domNodes`, byte-for-byte equivalent to Python.
///   * The `semantic_anchor` strategy parses the supplied `html`. Python uses
///     BeautifulSoup; this port uses a deterministic regex extractor that matches
///     BeautifulSoup's `get_text(strip=True)` for well-formed (non-nested-inline)
///     heading/label text and any element's `aria-label`. Deeply nested inline
///     markup is the documented bounded edge (see API_PARITY_VALIDATION_REPORT.md).
library;

const int _maxCandidates = 100;
const int _maxAnchors = 200;

final RegExp _idTokenRe = RegExp(r'#([a-zA-Z0-9_-]+)');
final RegExp _classTokenRe = RegExp(r'\.([a-zA-Z0-9_-]+)');
final RegExp _headingRe = RegExp(
  r'<(h1|h2|h3|label)\b[^>]*>([\s\S]*?)</\1>',
  caseSensitive: false,
);
final RegExp _ariaRe = RegExp(
  '''aria-label\\s*=\\s*("([^"]*)"|'([^']*)')''',
  caseSensitive: false,
);
final RegExp _tagStripRe = RegExp(r'<[^>]*>');

/// Healing token: `#id` or `.class` with both `-` and `_` mapped to spaces,
/// lower-cased; otherwise the trimmed lower-cased selector.
String _selectorTokenHealing(String selector) {
  final id = _idTokenRe.firstMatch(selector);
  if (id != null) {
    return id.group(1)!.replaceAll('-', ' ').replaceAll('_', ' ').toLowerCase();
  }
  final cls = _classTokenRe.firstMatch(selector);
  if (cls != null) {
    return cls
        .group(1)!
        .replaceAll('-', ' ')
        .replaceAll('_', ' ')
        .toLowerCase();
  }
  return selector.trim().toLowerCase();
}

/// Anchor token: like [_selectorTokenHealing] but maps only `-` to spaces,
/// matching Python `semantic_anchor_engine._selector_token`.
String _selectorTokenAnchor(String selector) {
  final id = _idTokenRe.firstMatch(selector);
  if (id != null) {
    return id.group(1)!.replaceAll('-', ' ').toLowerCase();
  }
  final cls = _classTokenRe.firstMatch(selector);
  if (cls != null) {
    return cls.group(1)!.replaceAll('-', ' ').toLowerCase();
  }
  return selector.trim().toLowerCase();
}

String _getTextStrip(String inner) {
  // Approximates BeautifulSoup get_text(strip=True) for non-nested content:
  // remove any tags, strip outer whitespace.
  return inner.replaceAll(_tagStripRe, '').trim();
}

String _anchorToSelector(Map<String, dynamic> anchor) {
  final text = (anchor['text'] ?? '').toString();
  final anchorType = (anchor['type'] ?? '').toString();
  final clipped = text.length > 200 ? text.substring(0, 200) : text;
  if (anchorType == 'aria') {
    return "[aria-label='$clipped']";
  }
  return "$anchorType:has-text('$clipped')";
}

/// Port of `build_semantic_anchor(selector, html)`.
Map<String, dynamic> buildSemanticAnchor(String selector, String html) {
  final src = html;
  final anchors = <Map<String, dynamic>>[];

  for (final m in _headingRe.allMatches(src)) {
    if (anchors.length >= _maxAnchors) break;
    final tag = m.group(1)!.toLowerCase();
    final text = _getTextStrip(m.group(2)!);
    if (text.isNotEmpty) {
      anchors.add(<String, dynamic>{
        'type': tag,
        'text': text.length > 500 ? text.substring(0, 500) : text,
      });
    }
  }

  var ariaCount = 0;
  for (final m in _ariaRe.allMatches(src)) {
    if (ariaCount >= _maxAnchors) break;
    ariaCount++;
    final value = m.group(2) ?? m.group(3) ?? '';
    anchors.add(<String, dynamic>{
      'type': 'aria',
      'text': value.length > 500 ? value.substring(0, 500) : value,
    });
  }

  final token = _selectorTokenAnchor(selector);
  final sorted = List<Map<String, dynamic>>.from(anchors)
    ..sort((a, b) {
      final t = (a['type'] as String).compareTo(b['type'] as String);
      if (t != 0) return t;
      return (a['text'] as String).compareTo(b['text'] as String);
    });

  final matched = <Map<String, dynamic>>[];
  for (final a in sorted) {
    if (token.isNotEmpty &&
        (a['text'] as String).toLowerCase().contains(token)) {
      matched.add(a);
    }
  }

  return <String, dynamic>{
    'selector': selector,
    'anchors': sorted,
    'matched': matched.take(20).toList(),
    'bounded': true,
  };
}

/// Port of `heal_selector(selector, dom_nodes, html="")`.
///
/// Returns a bounded map: `original`, `healed_selector`, `strategy`,
/// `candidates` (first 10), `bounded`.
Map<String, dynamic> healSelector(
  String selector,
  List<Map<String, dynamic>> domNodes, {
  String html = '',
}) {
  final strategies = <Map<String, dynamic>>[];

  final anchor = buildSemanticAnchor(selector, html);
  final matched = anchor['matched'] as List<dynamic>;
  if (matched.isNotEmpty) {
    final healed = _anchorToSelector(matched[0] as Map<String, dynamic>);
    strategies.add(<String, dynamic>{
      'strategy': 'semantic_anchor',
      'selector': healed,
    });
  }

  for (final node in domNodes.take(_maxCandidates)) {
    final text = (node['text'] ?? '').toString().toLowerCase();
    final tag = (node['tag'] ?? 'div').toString();
    final token = _selectorTokenHealing(selector);
    if (token.isNotEmpty && text.contains(token)) {
      final raw = (node['text'] ?? '').toString();
      final clip = raw.length > 100 ? raw.substring(0, 100) : raw;
      strategies.add(<String, dynamic>{
        'strategy': 'text_anchor',
        'selector': "$tag:has-text('$clip')",
      });
      break;
    }
  }

  for (final node in domNodes.take(_maxCandidates)) {
    final attrs = node['attrs'];
    if (attrs is Map) {
      final keys = attrs.keys.map((k) => k.toString()).toList()..sort();
      for (final key in keys) {
        if (key == 'aria-label' ||
            key == 'data-testid' ||
            key == 'name' ||
            key == 'id') {
          final value = (attrs[key] ?? '').toString();
          final clip = value.length > 200 ? value.substring(0, 200) : value;
          strategies.add(<String, dynamic>{
            'strategy': 'attribute_anchor',
            'selector': "[$key='$clip']",
          });
          break;
        }
      }
    }
    if (strategies.isNotEmpty) break;
  }

  if (strategies.isEmpty) {
    final parentTag =
        domNodes.isNotEmpty ? (domNodes[0]['tag'] ?? 'div').toString() : 'div';
    strategies.add(<String, dynamic>{
      'strategy': 'structural_fallback',
      'selector': parentTag,
    });
  }

  final healed = strategies[0];
  return <String, dynamic>{
    'original': selector,
    'healed_selector': healed['selector'],
    'strategy': healed['strategy'],
    'candidates': strategies.take(10).toList(),
    'bounded': true,
  };
}
