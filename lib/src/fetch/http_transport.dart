/// Transport abstraction for HTTP operations.
abstract class HttpTransport {
  Future<Map<String, dynamic>> fetch(String url);
  static HttpTransport getDefault() => _DefaultHttpTransport();
}

class _DefaultHttpTransport implements HttpTransport {
  @override
  Future<Map<String, dynamic>> fetch(String url) async {
    try {
      final uri = Uri.parse(url);
      final client = HttpClient();
      client.connectionTimeout = Duration(seconds: 30);
      final request = await client.getUrl(uri);
      request.headers.set('User-Agent', 'WebWeaveX/3.0.0');
      final response = await request.close().timeout(Duration(seconds: 30));
      final body = await response.transform(utf8.decoder).join();
      client.close();
      return {'text': body, 'status': response.statusCode, 'contentType': response.headers.contentType?.mimeType ?? 'text/plain', 'ok': response.statusCode >= 200 && response.statusCode < 400, 'error': ''};
    } catch (e) {
      return {'text': '', 'status': 0, 'contentType': 'text/plain', 'ok': false, 'error': e.toString()};
    }
  }
}
