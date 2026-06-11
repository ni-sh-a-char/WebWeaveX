/// Port of core/interaction/pagination_engine.py: extract_paginated_content.
///
/// Python's `page: Any` is a duck-typed live/test page object probed with
/// getattr/hasattr. This port models it as a `Map<String, dynamic>?` whose
/// keys mirror the Python attribute names exactly (`url`, `_test_url`,
/// `_test_next_url`, `_test_paginate`, `click`):
///   * getattr(page, name, default) -> page.containsKey(name) ? page[name] : default
///   * hasattr(page, name)          -> page.containsKey(name)
///   * page.click(sel) / page._test_paginate(url) -> the map value is a
///     Dart `Function` invoked via `Function.apply`
///   * `page._test_url = current_url` -> `page['_test_url'] = currentUrl`
/// The returned dict is byte-identical to Python for equivalent page hooks.
library;

const int maxPages = 100;

/// Python `str(value)` for the value kinds reachable here (page attribute
/// values: typically str; None/bool covered for fidelity).
String _pyStr(dynamic value) {
  if (value == null) return 'None';
  if (value is bool) return value ? 'True' : 'False';
  return value.toString();
}

/// Port of pagination_engine.extract_paginated_content.
Map<String, dynamic> extractPaginatedContent(
  Map<String, dynamic>? page,
  String nextSelector,
) {
  final Set<String> visited = <String>{};
  final List<Map<String, dynamic>> pages = <Map<String, dynamic>>[];

  String currentUrl = '';

  if (page != null) {
    currentUrl = _pyStr(page.containsKey('_test_url')
        ? page['_test_url']
        : (page.containsKey('url') ? page['url'] : ''));
  }

  while (pages.length < maxPages) {
    if (visited.contains(currentUrl)) {
      break;
    }

    visited.add(currentUrl);

    pages.add(<String, dynamic>{
      'url': currentUrl,
      'order': pages.length,
    });

    if (nextSelector.isEmpty) {
      break;
    }

    if (page != null && page.containsKey('click')) {
      try {
        Function.apply(page['click'] as Function, <dynamic>[nextSelector]);
      } catch (_) {
        break;
      }
    }

    String nextUrl = _pyStr(page != null && page.containsKey('_test_next_url')
        ? page['_test_next_url']
        : '');

    if (nextUrl.isEmpty || nextUrl == currentUrl) {
      if (page != null && page.containsKey('_test_paginate')) {
        final dynamic paginated = Function.apply(
          page['_test_paginate'] as Function,
          <dynamic>[currentUrl],
        );
        // Python assigns the raw return; `not next_url` treats None and ""
        // the same, so a null return is coerced to "" here.
        nextUrl = paginated == null ? '' : paginated as String;
      }
    }

    if (nextUrl.isEmpty || visited.contains(nextUrl)) {
      break;
    }

    currentUrl = nextUrl;
    if (page != null && page.containsKey('_test_url')) {
      page['_test_url'] = currentUrl;
    }
  }

  return <String, dynamic>{
    'pages': pages,
    'visited_count': visited.length,
    'loop_prevented': pages.length < maxPages,
    'bounded': true,
  };
}
