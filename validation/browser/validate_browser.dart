import 'dart:io';

import 'package:webweavex/webweavex.dart';

Future<void> main() async {
  final session = createRuntimeSession({'headers': {'x-test': '1'}});
  final path = '${Directory.current.path}/validation/browser/.session-test.kaalka';
  persistRuntimeSession(path, session, 'browser-test-key');
  final restored = restoreRuntimeSession(path, 'browser-test-key');

  final snapshot = await captureRuntimeSnapshot('https://example.com', session: session);
  final identity = buildBrowserIdentity(snapshot);
  final spa = stabilizeSpaDom('<div data-reactroot>hello</div>', route: '/');

  final results = {
    'session_roundtrip': restored['session_id'] == session['session_id'],
    'snapshot_bounded': snapshot['bounded'] == true,
    'identity_stable': identity['runtime_identity'] == buildBrowserIdentity(snapshot)['runtime_identity'],
    'spa_framework': spa['framework'] == 'react',
    'spa_hash': (spa['stable_dom_hash'] as String).isNotEmpty,
  };

  print('PASS $results');
  if (!results.values.every((v) => v == true)) exit(1);
}
