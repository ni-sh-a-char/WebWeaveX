import 'dart:io';

import 'package:test/test.dart';
import 'package:webweavex/src/browser/render_page.dart';

/// Exercises the HTTP *success* path of [renderPage] against a local loopback
/// server (127.0.0.1, ephemeral port) — no external network is touched.
void main() {
  late HttpServer server;
  late String base;

  setUp(() async {
    server = await HttpServer.bind(InternetAddress.loopbackIPv4, 0);
    base = 'http://127.0.0.1:${server.port}';
    server.listen((HttpRequest req) async {
      if (req.uri.path == '/large') {
        // Body larger than the 500000-char truncation threshold.
        req.response.write('x' * 600000);
      } else {
        req.response
          ..statusCode = 200
          ..write('<html><body>ok</body></html>');
      }
      await req.response.close();
    });
  });

  tearDown(() async {
    await server.close(force: true);
  });

  test('renderPage returns available body on 200 response', () async {
    final result = await renderPage('$base/');
    expect(result['available'], isTrue);
    expect(result['status'], 200);
    expect(result['html'], contains('ok'));
    expect(result['url'], '$base/');
  });

  test('renderPage truncates bodies over 500000 chars', () async {
    final result = await renderPage('$base/large');
    expect(result['available'], isTrue);
    expect((result['html'] as String).length, 500000);
  });
}
