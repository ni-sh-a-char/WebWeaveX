/// Simple web crawler using the transport abstraction.
class Crawler {
  final HttpTransport _transport;
  final Set<String> _visited = {};
  final List<String> _discovered = [];
  Crawler({HttpTransport? transport}) : _transport = transport ?? HttpTransport.getDefault();
  Map<String, dynamic> crawl(String url) {
    _crawlRecursive(url, 0);
    return {'visited': _visited.toList(), 'discovered': List<String>.from(_discovered)};
  }
  void _crawlRecursive(String url, int depth) {
    if (depth > 3 || _visited.contains(url)) return;
    _visited.add(url);
    _transport.fetch(url).then((resp) {
      if (resp['ok'] != true) return;
      final text = resp['text'] as String? ?? '';
      for (final m in RegExp(r'href="([^"]+)"').allMatches(text)) {
        final link = m.group(1)!;
        if (!_visited.contains(link)) _discovered.add(link);
      }
    });
  }
}
