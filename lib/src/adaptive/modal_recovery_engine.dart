/// Port of core/adaptive/modal_recovery_engine.py: recover_modal_runtime.
///
/// Python's `page: Any` is a duck-typed live/test page object probed with
/// getattr/hasattr. This port models it as a `Map<String, dynamic>?` whose
/// keys mirror the Python attribute names exactly (`_test_modals`, `click`):
///   * hasattr(page, name) -> page.containsKey(name)
///   * page.click(selector) -> the map value is a Dart `Function` invoked
///     via `Function.apply` (exceptions swallowed, as in Python)
///   * `page._test_modals = []` -> `page['_test_modals'] = []`
/// The returned dict is byte-identical to Python for equivalent page hooks.
library;

const int maxRetries = 5;

const List<String> _modalCloseSelectors = <String>[
  '#cookie-accept',
  "[aria-label='Close']",
  'button.accept',
  '.modal-close',
];

/// Python `s.strip(chars)`: removes leading and trailing characters that are
/// members of [chars] (a character set, not a prefix/suffix).
String _stripChars(String s, String chars) {
  int start = 0;
  int end = s.length;
  while (start < end && chars.contains(s[start])) {
    start++;
  }
  while (end > start && chars.contains(s[end - 1])) {
    end--;
  }
  return s.substring(start, end);
}

/// Port of modal_recovery_engine.recover_modal_runtime.
Map<String, dynamic> recoverModalRuntime(
  Map<String, dynamic>? page, {
  String html = '',
}) {
  final List<Map<String, dynamic>> recovered = <Map<String, dynamic>>[];
  int retries = 0;

  List<dynamic> modals = <dynamic>[];
  if (page != null && page.containsKey('_test_modals')) {
    modals = List<dynamic>.from(page['_test_modals'] as List<dynamic>);
  }

  for (final String selector in _modalCloseSelectors) {
    if (retries >= maxRetries) {
      break;
    }

    if (_selectorInHtml(selector, html) || modals.isNotEmpty) {
      if (page != null && page.containsKey('click')) {
        try {
          Function.apply(page['click'] as Function, <dynamic>[selector]);
        } catch (_) {
          // Python: except Exception: pass
        }
      }

      if (page != null && page.containsKey('_test_modals')) {
        page['_test_modals'] = <dynamic>[];
      }

      recovered.add(<String, dynamic>{
        'selector': selector,
        'recovered': true,
      });
      retries += 1;
      break;
    }
  }

  return <String, dynamic>{
    'recovered': recovered,
    'retries': retries,
    'bounded': true,
  };
}

/// Port of modal_recovery_engine._selector_in_html.
bool _selectorInHtml(String selector, String html) {
  final String token =
      _stripChars(selector, '#.[]').split("'")[0].split('"')[0];
  return html.toLowerCase().contains(token.toLowerCase());
}
