/// Minimal BeautifulSoup-parity HTML tree — Dart port of the JavaScript
/// runtime's PySoup, which is byte-certified against Python bs4
/// (html.parser) on 130 real internet pages + 14 malformed-HTML torture
/// cases (cross_language_verifier/extraction_certification.json).
///
/// Encodes the certified html.parser/bs4 rules:
/// - data coalescing with whitespace-only collapse (ASCII_SPACES -> "\n"/" ",
///   NBSP preserved, pre/textarea exempt)
/// - literal "<" not followed by letter / "/" / "!" / "?" is data
/// - quote-aware tag-end scan (">" inside quoted attribute values)
/// - unquoted attribute trailing "/" is not self-closing
/// - script/style raw-text close scan without whole-document lowercasing
/// - get_text excludes script/style/template/rt/rp contents
/// - full HTML5 named entity table (@generated from Python)
library;

import '../determinism/normalization_core.dart' show codePointCompare;
import 'html_entities.dart';

const Set<String> _voidElements = {
  'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input',
  'link', 'meta', 'param', 'source', 'track', 'wbr',
};

// Python html._charref — semicolon optional, exact name charset.
final RegExp _charref =
    RegExp(r'&(#[0-9]+;?|#[xX][0-9a-fA-F]+;?|[^\t\n\f <&#;]{1,32};?)');

/// Full Python html.unescape (used by html.parser convert_charrefs and for
/// attribute values).
String htmlUnescape(String s) {
  if (!s.contains('&')) return s;
  return s.replaceAllMapped(_charref, (m) {
    final ent = m.group(1)!;
    if (ent.startsWith('#')) {
      final hex = ent.length > 1 && (ent[1] == 'x' || ent[1] == 'X');
      var digits = ent.substring(hex ? 2 : 1);
      if (digits.endsWith(';')) digits = digits.substring(0, digits.length - 1);
      final num = int.parse(digits, radix: hex ? 16 : 10);
      final mapped = invalidCharrefs[num];
      if (mapped != null) return mapped;
      if ((num >= 0xd800 && num <= 0xdfff) || num > 0x10ffff) {
        return String.fromCharCode(0xfffd);
      }
      if (invalidCodepoints.contains(num)) return '';
      return String.fromCharCode(num);
    }
    // named charref: exact match first (with or without semicolon) ...
    if (ent.endsWith(';')) {
      final v = htmlEntities[ent.substring(0, ent.length - 1)];
      if (v != null) return v;
    } else {
      final v = htmlEntitiesNoSemi[ent];
      if (v != null) return v;
    }
    // ... else longest matching semicolonless name (Python prefix scan).
    for (var x = ent.length - 1; x >= 2; x--) {
      final v = htmlEntitiesNoSemi[ent.substring(0, x)];
      if (v != null) return v + ent.substring(x);
    }
    return '&$ent';
  });
}

/// Python str.strip() whitespace (NOT Dart trim(): U+FEFF is not whitespace
/// in Python; U+001C-001F are).
final RegExp _pyWsLead = RegExp('^[\\t-\\r\\x1c-\\x1f '
    '\\x85\\xa0\\u1680\\u2000-\\u200a\\u2028\\u2029\\u202f\\u205f\\u3000]+');
final RegExp _pyWsTrail = RegExp('[\\t-\\r\\x1c-\\x1f '
    '\\x85\\xa0\\u1680\\u2000-\\u200a\\u2028\\u2029\\u202f\\u205f\\u3000]+\$');

String pyStrip(String s) =>
    s.replaceFirst(_pyWsLead, '').replaceFirst(_pyWsTrail, '');

/// Python `s[:n]` — slices by CODE POINTS, not UTF-16 units.
String pyTruncate(String s, int n) {
  if (s.length <= n) return s; // <= n UTF-16 units implies <= n code points
  final it = s.runes.iterator;
  var count = 0;
  var endUnits = 0;
  while (it.moveNext()) {
    count++;
    endUnits = it.rawIndex + it.currentSize;
    if (count == n) break;
  }
  return count < n ? s : s.substring(0, endUnits);
}

/// A text node whose bs4 string-container type (Script/Stylesheet/
/// TemplateString/RubyTextString/RubyParenthesisString) excludes it from
/// get_text — decided at PARSE time from the ancestor chain, exactly like
/// bs4's string_container stack.
class HiddenString {
  HiddenString(this.text);
  final String text;
}

class SoupTag {
  SoupTag(this.name);

  final String name;
  final Map<String, dynamic> attrs = {};
  final List<Object> children = []; // SoupTag | String | HiddenString
  SoupTag? parent;

  dynamic operator [](String key) => attrs[key];

  String? get(String key) {
    final v = attrs[key];
    if (v == null) return null;
    if (v is List) return v.join(' ');
    return v.toString();
  }

  /// bs4 get_text: descendant strings joined by [sep]; excludes
  /// script/style/template/rt/rp (exact-type string-container filter).
  String getText({String sep = '', bool strip = false}) {
    final parts = <String>[];
    void walk(Object node) {
      if (node is HiddenString) return;
      if (node is String) {
        final t = strip ? pyStrip(node) : node;
        if (strip ? t.isNotEmpty : node.isNotEmpty) parts.add(t);
        return;
      }
      for (final c in (node as SoupTag).children) {
        walk(c);
      }
    }

    for (final c in children) {
      walk(c);
    }
    return parts.join(sep);
  }

  /// bs4 `.text`.
  String get text => getText();

  List<SoupTag> findAll(Object? name, {int? limit}) {
    Set<String>? names;
    String? single;
    if (name is List) {
      names = {for (final n in name) n.toString().toLowerCase()};
    } else if (name is String) {
      single = name.toLowerCase();
    }
    // name == null or name == true -> match every tag (bs4 find_all(True))
    final out = <SoupTag>[];
    void walk(Object node) {
      if (node is! SoupTag) return;
      if (limit != null && out.length >= limit) return;
      final tag = node;
      final matches = names != null
          ? names.contains(tag.name)
          : (single == null || tag.name == single);
      if (matches) out.add(tag);
      for (final c in tag.children) {
        walk(c);
      }
    }

    for (final c in children) {
      walk(c);
    }
    return limit != null && out.length > limit ? out.sublist(0, limit) : out;
  }

  SoupTag? find(Object? name) {
    final r = findAll(name, limit: 1);
    return r.isEmpty ? null : r.first;
  }
}

class Soup extends SoupTag {
  Soup(String html) : super('[document]') {
    _parseInto(html);
  }

  SoupTag? get title => find('title');

  int _ampFails = 0;

  void _parseInto(String html) {
    SoupTag cur = this;
    var i = 0;
    final n = html.length;
    var buf = StringBuffer();

    void flush() {
      if (buf.isEmpty) return;
      var text = buf.toString();
      buf = StringBuffer();
      // bs4 endData ASCII_SPACES rule
      var strippable = true;
      for (final u in text.codeUnits) {
        if (u != 0x20 && u != 0x0a && u != 0x09 && u != 0x0c && u != 0x0d) {
          strippable = false;
          break;
        }
      }
      if (strippable) {
        SoupTag? node = cur;
        var preserve = false;
        while (node != null) {
          if (node.name == 'pre' || node.name == 'textarea') {
            preserve = true;
            break;
          }
          node = node.parent;
        }
        if (!preserve) text = text.contains('\n') ? '\n' : ' ';
      }
      // bs4 string-container typing: any script/style/template/rt/rp
      // ancestor makes the string invisible to get_text.
      SoupTag? anc = cur;
      var hidden = false;
      while (anc != null) {
        final a = anc.name;
        if (a == 'script' || a == 'style' || a == 'template' ||
            a == 'rt' || a == 'rp') {
          hidden = true;
          break;
        }
        anc = anc.parent;
      }
      cur.children.add(hidden ? HiddenString(text) : text);
    }

    final letter = RegExp(r'[a-zA-Z]');
    final nameRe = RegExp(r'^\s*([a-zA-Z][a-zA-Z0-9:-]*)');
    final attrRe = RegExp(
        '([a-zA-Z_:][-a-zA-Z0-9_:.]*)\\s*(?:=\\s*("([^"]*)"|\'([^\']*)\'|[^\\s"\'>]+))?');
    final digitRe = RegExp(r'[0-9]');
    final hexRe = RegExp(r'[0-9a-fA-F]');
    final entStartRe = RegExp(r'[a-zA-Z]');
    final entBodyRe = RegExp(r'[-.a-zA-Z0-9]');

    String charrefChr(int num) {
      final mapped = invalidCharrefs[num];
      if (mapped != null) return mapped;
      if ((num >= 0xd800 && num <= 0xdfff) || num > 0x10ffff) {
        return String.fromCharCode(0xfffd);
      }
      return String.fromCharCode(num);
    }

    // html.parser text tokenization for "&": returns new index, or -1 to
    // signal defer-to-EOF (incomplete charref with no ";" remaining — the
    // rest of the document is flushed as raw data, exactly like html.parser's
    // buffered goahead + close()).
    int handleAmp(int pos) {
      final c2 = pos + 1 < n ? html[pos + 1] : '';
      if (c2 == '#') {
        var k = pos + 2;
        final isHex = k < n && (html[k] == 'x' || html[k] == 'X');
        if (isHex) k++;
        final dstart = k;
        final dre = isHex ? hexRe : digitRe;
        while (k < n && dre.hasMatch(html[k])) {
          k++;
        }
        final hasDigits = k > dstart;
        final next = k < n ? html[k] : null;
        if (hasDigits && next == ';') {
          buf.write(charrefChr(
              int.parse(html.substring(dstart, k), radix: isHex ? 16 : 10)));
          return k + 1;
        }
        if (hasDigits && next != null && !hexRe.hasMatch(next)) {
          buf.write(charrefChr(
              int.parse(html.substring(dstart, k), radix: isHex ? 16 : 10)));
          return k;
        }
        // Failed charref: html.parser consumes "&#" (when a ";" remains
        // anywhere) and BREAKS the parsing pass. bs4 drives two passes
        // (feed + close), so the SECOND failed "&#" dumps the rest of the
        // document as raw data; with no ";" remaining, the dump is
        // immediate and includes the "&#".
        if (html.indexOf(';', pos) >= 0) {
          buf.write('&#');
          _ampFails++;
          if (_ampFails >= 2) {
            buf.write(html.substring(pos + 2));
            return -2; // defer: "&#" already consumed
          }
          return pos + 2;
        }
        return -1;
      }
      if (c2.isNotEmpty && entStartRe.hasMatch(c2)) {
        var k = pos + 2;
        while (k < n && entBodyRe.hasMatch(html[k])) {
          k++;
        }
        final name = html.substring(pos + 1, k);
        if (k >= n) return -1; // incomplete entityref at EOF -> defer
        final value = htmlEntities[name];
        if (html[k] == ';') {
          buf.write(value ?? '&$name');
          return k + 1;
        }
        buf.write(value ?? '&$name');
        return k;
      }
      buf.write('&');
      return pos + 1;
    }

    while (i < n) {
      // Scan text: handle "&" inline (bs4 handle_charref/handle_entityref
      // semantics differ from html.unescape; attributes still use
      // htmlUnescape below).
      var lt = -1;
      var t = i;
      var deferred = false;
      while (t < n) {
        final ltp = html.indexOf('<', t);
        final amp = html.indexOf('&', t);
        if (amp < 0 || (ltp >= 0 && ltp < amp)) {
          if (ltp < 0) {
            buf.write(html.substring(t));
            t = n;
          } else {
            buf.write(html.substring(t, ltp));
            lt = ltp;
          }
          break;
        }
        buf.write(html.substring(t, amp));
        final nt = handleAmp(amp);
        if (nt == -1) {
          buf.write(html.substring(amp));
          deferred = true;
          break;
        }
        if (nt == -2) {
          deferred = true;
          break;
        }
        t = nt;
      }
      if (deferred) break;
      if (lt < 0) {
        break;
      }
      i = lt;
      // html.parser: "<" not followed by a letter, "/", "!" or "?" is data.
      final nxt = lt + 1 < n ? html[lt + 1] : '';
      if (!(letter.hasMatch(nxt) || nxt == '/' || nxt == '!' || nxt == '?')) {
        buf.write('<');
        i = lt + 1;
        continue;
      }
      if (html.startsWith('<!--', lt)) {
        flush();
        final end = html.indexOf('-->', lt + 4);
        i = end < 0 ? n : end + 3;
        continue;
      }
      if (html.startsWith('<!', lt) || html.startsWith('<?', lt)) {
        flush();
        final end = html.indexOf('>', lt);
        i = end < 0 ? n : end + 1;
        continue;
      }
      // Quote-aware tag-end scan.
      var gt = -1;
      String? q;
      for (var k = lt + 1; k < n; k++) {
        final c = html[k];
        if (q != null) {
          if (c == q) q = null;
        } else if (c == '"' || c == "'") {
          q = c;
        } else if (c == '>') {
          gt = k;
          break;
        }
      }
      if (gt < 0) {
        buf.write(htmlUnescape(html.substring(lt)));
        break;
      }
      final raw = html.substring(lt + 1, gt);
      i = gt + 1;
      if (raw.startsWith('/')) {
        flush();
        final closeName = raw.substring(1).trim().toLowerCase();
        SoupTag? node = cur;
        while (node != null && node.name != closeName) {
          node = node.parent;
        }
        if (node != null && node.parent != null) {
          cur = node.parent!;
        } else if (identical(node, cur) && cur.parent != null) {
          cur = cur.parent!;
        }
        continue;
      }
      flush();
      final nameM = nameRe.firstMatch(raw);
      if (nameM == null) continue;
      final tagName = nameM.group(1)!.toLowerCase();
      final tag = SoupTag(tagName);
      tag.parent = cur;
      // html.parser: trailing "/" is self-closing only when NOT glued to an
      // unquoted attribute value (href=/dev/ keeps its slash).
      var attrStr = raw.substring(nameM.group(0)!.length);
      var selfClose = false;
      final slashTrail = RegExp(r'/\s*$');
      if (slashTrail.hasMatch(attrStr)) {
        final beforeSlash = attrStr.replaceFirst(slashTrail, '');
        if (beforeSlash.isEmpty ||
            RegExp(r'''[\s"']$''').hasMatch(beforeSlash)) {
          selfClose = true;
          attrStr = beforeSlash;
        }
      }
      for (final am in attrRe.allMatches(attrStr)) {
        final key = am.group(1)!.toLowerCase();
        dynamic val;
        if (am.group(2) == null) {
          val = '';
        } else if (am.group(3) != null) {
          val = htmlUnescape(am.group(3)!);
        } else if (am.group(4) != null) {
          val = htmlUnescape(am.group(4)!);
        } else {
          val = htmlUnescape(am.group(2)!);
        }
        if (key == 'class') {
          val = val
              .toString()
              .split(RegExp(r'\s+'))
              .where((c) => c.isNotEmpty)
              .toList();
        }
        tag.attrs[key] = val;
      }
      cur.children.add(tag);
      if (tagName == 'script' || tagName == 'style') {
        // Case-insensitive close scan without lowercasing the whole document
        // (Unicode lowercasing can change string length, e.g. U+0130).
        final closeM =
            RegExp('</\\s*$tagName', caseSensitive: false).firstMatch(html.substring(i));
        final closeIdx = closeM == null ? -1 : i + closeM.start;
        final rawText = html.substring(i, closeIdx < 0 ? n : closeIdx);
        if (rawText.isNotEmpty) tag.children.add(HiddenString(rawText));
        if (closeIdx < 0) break;
        final closeGt = html.indexOf('>', closeIdx);
        i = closeGt < 0 ? n : closeGt + 1;
        continue;
      }
      if (!selfClose && !_voidElements.contains(tagName)) cur = tag;
    }
    flush();
  }
}

/// Sorted-set helper matching Python `sorted(set(xs))` (code-point order).
List<String> sortedSet(Iterable<String> xs) {
  final out = xs.toSet().toList()..sort(codePointCompare);
  return out;
}
