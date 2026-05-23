import '../determinism/dom_stabilization.dart';
import 'render_page.dart';

Future<Map<String, dynamic>> captureRuntime(String url) async {
  final rendered = await renderPage(url);
  final html = rendered['html'] as String? ?? '';
  final domHash = html.isNotEmpty ? computeStableDomHash(html) : '';
  return {
    'url': url,
    'available': rendered['available'] ?? false,
    'dom_hash': domHash,
    'routes': [url],
    'network': <Map<String, String>>[
      {'url': url, 'method': 'GET'},
    ],
    'storage': <String, dynamic>{},
  };
}

Future<String> captureDom(String url) async {
  final c = await captureRuntime(url);
  return c['dom_hash'] as String? ?? '';
}
