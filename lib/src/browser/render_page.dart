import 'dart:convert';

import 'package:http/http.dart' as http;

/// Bounded HTTP fetch (Playwright optional in host environment).
Future<Map<String, dynamic>> renderPage(String url) async {
  try {
    final res =
        await http.get(Uri.parse(url)).timeout(const Duration(seconds: 15));
    final body = res.body;
    return {
      'url': url,
      'status': res.statusCode,
      'html': body.length > 500000 ? body.substring(0, 500000) : body,
      'available': true,
    };
  } catch (_) {
    return {'url': url, 'available': false, 'html': ''};
  }
}

String routesFingerprint(String url) =>
    base64Encode(utf8.encode(url)).substring(0, 16);
