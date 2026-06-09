// High-coverage unit tests for lib/src/browser/* target files.
//
// NETWORK SAFETY: captureRuntime/extractWeb/render_page/etc. internally call
// renderPage(url) which performs an http.get wrapped in try/catch. We never
// hit a real server: every URL used here fails to connect/parse *immediately*
// (invalid scheme, bad host, or unparseable), so renderPage falls into its
// catch branch and returns {available:false, html:''}. This deterministically
// exercises the OFFLINE/degraded path of every network-touching function
// without any real HTTP round-trip.

import 'dart:convert';
import 'dart:io';

import 'package:test/test.dart';
import 'package:webweavex/webweavex.dart';

/// URLs that fail synchronously / near-instantly (no real network round-trip).
const _offlineUrls = <String>[
  'ftp://wwx.invalid/resource', // unsupported scheme -> throws fast
  'not a real url at all', // unparseable for http.get -> throws fast
  'http://0.0.0.0:1/blocked', // connection refused instantly
];

void main() {
  group('render_page', () {
    test('renderPage degraded/offline path returns available:false', () async {
      for (final u in _offlineUrls) {
        final r = await renderPage(u);
        expect(r['url'], u);
        expect(r['available'], isFalse);
        expect(r['html'], '');
      }
    });

    test('routesFingerprint is deterministic, 16 chars, base64', () {
      final fp = routesFingerprint('https://example.com/path');
      expect(fp.length, 16);
      expect(fp, routesFingerprint('https://example.com/path'));
      // URLs that differ within the first ~12 bytes => differ in first 16 b64.
      expect(fp, isNot(routesFingerprint('zzz://other-host/path')));
      // It is the prefix of the base64 encoding of the URL bytes.
      final full = base64Encode(utf8.encode('https://example.com/path'));
      expect(fp, full.substring(0, 16));
    });
  });

  group('capture_runtime', () {
    test('captureRuntime offline yields empty dom_hash + bounded shape',
        () async {
      final c = await captureRuntime('ftp://wwx.invalid/x');
      expect(c['url'], 'ftp://wwx.invalid/x');
      expect(c['available'], isFalse);
      expect(c['dom_hash'], ''); // html empty -> empty hash branch
      expect(c['routes'], <String>['ftp://wwx.invalid/x']);
      final network = c['network'] as List;
      expect(network, hasLength(1));
      expect((network.first as Map)['method'], 'GET');
      expect((network.first as Map)['url'], 'ftp://wwx.invalid/x');
      expect(c['storage'], <String, dynamic>{});
    });

    test('captureDom offline returns empty string', () async {
      final dom = await captureDom('not a real url');
      expect(dom, '');
    });
  });

  group('spa_stabilizer', () {
    test('stabilizeSpaDom detects react', () {
      final r = stabilizeSpaDom('<div data-reactroot="">x</div>', route: '/r');
      expect(r['framework'], 'react');
      expect(r['bounded'], isTrue);
      expect(r['stabilized_html'], isA<String>());
      expect(r['stable_dom_hash'], isA<String>());
      expect(r['spa_fingerprint'], r['stable_dom_hash']);
      expect(r['route_hash'], isA<String>());
    });

    test('stabilizeSpaDom detects react via __REACT marker', () {
      final r = stabilizeSpaDom('<script>window.__REACT_DEVTOOLS=1</script>');
      expect(r['framework'], 'react');
    });

    test('stabilizeSpaDom detects vue', () {
      final r = stabilizeSpaDom('<div data-v-12ab>x</div>');
      expect(r['framework'], 'vue');
    });

    test('stabilizeSpaDom detects angular (ng-version)', () {
      final r = stabilizeSpaDom('<app ng-version="17.0.0"></app>');
      expect(r['framework'], 'angular');
    });

    test('stabilizeSpaDom detects angular (_ngcontent)', () {
      final r = stabilizeSpaDom('<div _ngcontent-abc>x</div>');
      expect(r['framework'], 'angular');
    });

    test('stabilizeSpaDom unknown framework is null; route affects route_hash',
        () {
      final a = stabilizeSpaDom('<div>plain html</div>', route: '/a');
      final b = stabilizeSpaDom('<div>plain html</div>', route: '/b');
      expect(a['framework'], isNull);
      // same html, same stable hash, but different route -> different route_hash
      expect(a['stable_dom_hash'], b['stable_dom_hash']);
      expect(a['route_hash'], isNot(b['route_hash']));
    });

    test('stabilizeSpaDom default route and empty html', () {
      final r = stabilizeSpaDom('');
      expect(r['framework'], isNull);
      expect(r['bounded'], isTrue);
    });
  });

  group('browser_identity', () {
    test('buildBrowserIdentity full captured map', () {
      final captured = <String, dynamic>{
        'url': 'https://x.test',
        'dom_hash': 'abc',
        'storage': <String, dynamic>{'k': 'v'},
        'routes': <dynamic>['/a', '/b'],
        'network': <dynamic>[
          <String, String>{'url': 'https://x.test', 'method': 'GET'},
        ],
      };
      final id = buildBrowserIdentity(captured);
      expect(id['runtime_identity'], isA<String>());
      expect(id['profile_hash'], isA<String>());
      expect(id['storage_hash'], isA<String>());
      expect(id['route_fingerprint'], isA<String>());
      expect(id['bounded'], isTrue);
      // determinism
      expect(buildBrowserIdentity(captured), id);
    });

    test('buildBrowserIdentity empty map exercises ?? fallbacks', () {
      final id = buildBrowserIdentity(<String, dynamic>{});
      expect(id['runtime_identity'], isA<String>());
      // network missing -> length 0 branch; storage/routes default
      expect(id['storage_hash'], isA<String>());
      expect(id['route_fingerprint'], isA<String>());
      expect(id['bounded'], isTrue);
    });

    test('buildBrowserIdentity network length feeds profile_hash', () {
      final one = buildBrowserIdentity(<String, dynamic>{
        'url': 'u',
        'network': <dynamic>[
          <String, String>{'url': 'u', 'method': 'GET'}
        ],
      });
      final two = buildBrowserIdentity(<String, dynamic>{
        'url': 'u',
        'network': <dynamic>[
          <String, String>{'url': 'u', 'method': 'GET'},
          <String, String>{'url': 'u2', 'method': 'POST'},
        ],
      });
      // different network lengths -> different profile hashes
      expect(one['profile_hash'], isNot(two['profile_hash']));
    });

    test('identityFromExtraction with browser_ir map', () {
      final env = <String, dynamic>{
        'browser_ir': <String, dynamic>{
          'runtime_identity': 'rid-123',
          'storage': <String, dynamic>{'token': 'abc'},
        },
      };
      final id = identityFromExtraction(env);
      expect(id['runtime_identity'], 'rid-123');
      expect(id['profile_hash'], isA<String>());
      expect(id['storage_hash'], isA<String>());
      expect(id['route_fingerprint'], isA<String>());
      expect(id['bounded'], isTrue);
    });

    test('identityFromExtraction missing browser_ir uses defaults', () {
      final id = identityFromExtraction(<String, dynamic>{});
      expect(id['runtime_identity'], ''); // ir empty -> '' default
      expect(id['storage_hash'], isA<String>());
      expect(id['bounded'], isTrue);
    });
  });

  group('authenticated_runtime + runtime_session (round-trip)', () {
    late Directory tmp;

    setUp(() {
      tmp = Directory.systemTemp.createTempSync('wwx_auth_test_');
    });

    tearDown(() {
      if (tmp.existsSync()) tmp.deleteSync(recursive: true);
    });

    test('save then load round-trips the session map', () {
      final path = '${tmp.path}/session.enc';
      final session = <String, dynamic>{
        'session_id': 'sid-1',
        'cookies': <dynamic>['c1', 'c2'],
      };
      final saved = saveAuthenticatedRuntime(path, session, 'key-1');
      expect(saved['saved'], isTrue);
      expect(saved['path'], path);
      expect(saved['bounded'], isTrue);
      expect(File(path).existsSync(), isTrue);
      // file wrapper contains 'encrypted'
      final wrapper =
          jsonDecode(File(path).readAsStringSync()) as Map<String, dynamic>;
      expect(wrapper.containsKey('encrypted'), isTrue);

      final loaded = loadAuthenticatedRuntime(path, 'key-1');
      expect(loaded['session_id'], 'sid-1');
      expect(loaded['cookies'], <dynamic>['c1', 'c2']);
    });

    test('loadAuthenticatedRuntime decodes string fallback branch', () {
      // Craft an encrypted payload whose decrypted content is a *quoted* JSON
      // string literal. decryptValue then returns a String (not a Map),
      // forcing loadAuthenticatedRuntime down its jsonDecode(string) fallback.
      final path = '${tmp.path}/stringfallback.enc';
      final raw = '"{\\"a\\":1,\\"b\\":2}"'; // bytes: "{\"a\":1,\"b\":2}"
      final encrypted = encryptValue(raw, 'k2');
      File(path).writeAsStringSync(jsonEncode(<String, String>{
        'encrypted': encrypted,
      }));
      final loaded = loadAuthenticatedRuntime(path, 'k2');
      expect(loaded, <String, dynamic>{'a': 1, 'b': 2});
    });

    test('rotateAuthenticatedSession re-encrypts under new key', () {
      final path = '${tmp.path}/rotate.enc';
      final session = <String, dynamic>{'session_id': 'sid-2', 'v': 42};
      saveAuthenticatedRuntime(path, session, 'old-key');

      final rotated = rotateAuthenticatedSession(path, 'old-key', 'new-key');
      expect(rotated['saved'], isTrue);
      expect(rotated['path'], path);

      // old key can no longer decrypt to valid content; new key can.
      final reloaded = loadAuthenticatedRuntime(path, 'new-key');
      expect(reloaded['session_id'], 'sid-2');
      expect(reloaded['v'], 42);
    });

    test('createRuntimeSession with no state uses defaults', () {
      final s = createRuntimeSession();
      expect(s['cookies'], <dynamic>[]);
      expect(s['headers'], <String, dynamic>{});
      expect(s['auth_tokens'], <dynamic>[]);
      expect(s['localStorage'], <String, dynamic>{});
      expect(s['sessionStorage'], <String, dynamic>{});
      expect(s['session_id'], isA<String>());
      expect(s['bounded'], isTrue);
    });

    test('createRuntimeSession with provided state preserves values', () {
      final s = createRuntimeSession(<String, dynamic>{
        'cookies': <dynamic>['x'],
        'headers': <String, dynamic>{'Auth': 'Bearer'},
        'auth_tokens': <dynamic>['t'],
        'localStorage': <String, dynamic>{'a': 1},
        'sessionStorage': <String, dynamic>{'b': 2},
      });
      expect(s['cookies'], <dynamic>['x']);
      expect(s['headers'], <String, dynamic>{'Auth': 'Bearer'});
      expect(s['auth_tokens'], <dynamic>['t']);
      expect(s['localStorage'], <String, dynamic>{'a': 1});
      expect(s['sessionStorage'], <String, dynamic>{'b': 2});
      expect(s['session_id'], isA<String>());
    });

    test('createRuntimeSession session_id is deterministic for same state', () {
      final a = createRuntimeSession(<String, dynamic>{
        'cookies': <dynamic>['x']
      });
      final b = createRuntimeSession(<String, dynamic>{
        'cookies': <dynamic>['x']
      });
      expect(a['session_id'], b['session_id']);
    });

    test('persist then restore runtime session', () {
      final path = '${tmp.path}/persist.enc';
      final session = createRuntimeSession(<String, dynamic>{
        'cookies': <dynamic>['ck'],
        'headers': <String, dynamic>{'H': '1'},
      });
      final p = persistRuntimeSession(path, session, 'pk');
      expect(p['path'], path);
      expect(p['session_id'], session['session_id']);
      expect(p['bounded'], isTrue);

      final restored = restoreRuntimeSession(path, 'pk');
      // restore rebuilds via createRuntimeSession; cookies preserved
      expect(restored['cookies'], <dynamic>['ck']);
      expect(restored['headers'], <String, dynamic>{'H': '1'});
      expect(restored['bounded'], isTrue);
    });
  });

  group('runtime_snapshot', () {
    test('captureRuntimeSnapshot offline default tick/session', () async {
      final snap = await captureRuntimeSnapshot('ftp://wwx.invalid/s');
      expect(snap['url'], 'ftp://wwx.invalid/s');
      expect(snap['available'], isFalse);
      expect(snap['snapshot_id'], isA<String>());
      expect(snap['captured_at_tick'], 0);
      expect(snap['bounded'], isTrue);
      // merged from captured
      expect(snap['routes'], <String>['ftp://wwx.invalid/s']);
    });

    test('captureRuntimeSnapshot with tick + session changes snapshot_id',
        () async {
      final base = await captureRuntimeSnapshot('ftp://wwx.invalid/s', tick: 0);
      final tickier =
          await captureRuntimeSnapshot('ftp://wwx.invalid/s', tick: 5);
      expect(base['snapshot_id'], isNot(tickier['snapshot_id']));

      final withSession = await captureRuntimeSnapshot(
        'ftp://wwx.invalid/s',
        tick: 0,
        session: <String, dynamic>{'session_id': 'sid-X'},
      );
      expect(base['snapshot_id'], isNot(withSession['snapshot_id']));
      expect(withSession['captured_at_tick'], 0);
    });

    test('compareRuntimeSnapshots equivalent when dom + routes match', () {
      final a = <String, dynamic>{
        'dom_hash': 'h1',
        'routes': <String>['/a'],
      };
      final b = <String, dynamic>{
        'dom_hash': 'h1',
        'routes': <String>['/a'],
      };
      final cmp = compareRuntimeSnapshots(a, b);
      expect(cmp['equivalent'], isTrue);
      expect(cmp['dom_match'], isTrue);
      expect(cmp['route_match'], isTrue);
      expect(cmp['bounded'], isTrue);
    });

    test('compareRuntimeSnapshots dom mismatch', () {
      final cmp = compareRuntimeSnapshots(
        <String, dynamic>{
          'dom_hash': 'h1',
          'routes': <String>['/a']
        },
        <String, dynamic>{
          'dom_hash': 'h2',
          'routes': <String>['/a']
        },
      );
      expect(cmp['equivalent'], isFalse);
      expect(cmp['dom_match'], isFalse);
      expect(cmp['route_match'], isTrue);
    });

    test('compareRuntimeSnapshots route mismatch', () {
      final cmp = compareRuntimeSnapshots(
        <String, dynamic>{
          'dom_hash': 'h1',
          'routes': <String>['/a']
        },
        <String, dynamic>{
          'dom_hash': 'h1',
          'routes': <String>['/b']
        },
      );
      expect(cmp['equivalent'], isFalse);
      expect(cmp['dom_match'], isTrue);
      expect(cmp['route_match'], isFalse);
    });

    test('compareRuntimeSnapshots two real offline snapshots are equivalent',
        () async {
      final s1 = await captureRuntimeSnapshot('ftp://wwx.invalid/s');
      final s2 = await captureRuntimeSnapshot('ftp://wwx.invalid/s');
      final cmp = compareRuntimeSnapshots(s1, s2);
      expect(cmp['equivalent'], isTrue);
    });
  });

  group('extract_web', () {
    test('extractWeb unauthenticated offline envelope shape', () async {
      final env = await extractWeb('ftp://wwx.invalid/page');
      expect(env['bounded'], isTrue);
      final runtime = env['runtime'] as Map<String, dynamic>;
      expect(runtime['available'], isFalse);
      expect((runtime['session'] as Map), isEmpty); // no auth -> empty meta
      final ir = env['browser_ir'] as Map<String, dynamic>;
      expect(ir['runtime_identity'], isA<String>());
      expect(env['unified_runtime_graph'], isA<Map>());
      expect(env['graph'], isA<Map>());
      expect(env['pipeline_hash'], isA<String>());
      expect(env['global_runtime_fingerprint'], isA<String>());
      expect(env.containsKey('semantic'), isFalse);
    });

    test('extractWeb with semanticRuntime adds semantic block', () async {
      final env =
          await extractWeb('ftp://wwx.invalid/page', semanticRuntime: true);
      final sem = env['semantic'] as Map<String, dynamic>;
      expect(sem['entities'], <dynamic>[]);
      expect(sem['bounded'], isTrue);
    });

    test('extractWeb authenticated loads session meta', () async {
      final tmp = Directory.systemTemp.createTempSync('wwx_extract_');
      try {
        final path = '${tmp.path}/sess.enc';
        // Session that includes cookies so cookie_count branch is exercised.
        saveAuthenticatedRuntime(
          path,
          <String, dynamic>{
            'session_id': 'sid',
            'cookies': <dynamic>['a', 'b', 'c'],
          },
          'ek',
        );
        final env = await extractWeb(
          'ftp://wwx.invalid/page',
          authenticated: true,
          sessionPath: path,
          encryptionKey: 'ek',
        );
        final session = (env['runtime'] as Map<String, dynamic>)['session']
            as Map<String, dynamic>;
        expect(session['session_loaded'], isTrue);
        expect(session['cookie_count'], 3);
      } finally {
        tmp.deleteSync(recursive: true);
      }
    });

    test('extractWeb authenticated but missing sessionPath skips session load',
        () async {
      // authenticated:true but no path/key -> the && guard is false branch
      final env =
          await extractWeb('ftp://wwx.invalid/page', authenticated: true);
      final session =
          (env['runtime'] as Map<String, dynamic>)['session'] as Map;
      expect(session, isEmpty);
    });

    test('extractWeb is deterministic for same url', () async {
      final a = await extractWeb('ftp://wwx.invalid/page');
      final b = await extractWeb('ftp://wwx.invalid/page');
      expect(a['pipeline_hash'], b['pipeline_hash']);
      expect(a['global_runtime_fingerprint'], b['global_runtime_fingerprint']);
    });
  });

  group('runtime_continuation', () {
    test('extractWithSession offline envelope', () async {
      final session = createRuntimeSession(<String, dynamic>{
        'cookies': <dynamic>['c'],
      });
      final env = await extractWithSession('ftp://wwx.invalid/c', session);
      expect(env['bounded'], isTrue);
      final runtime = env['runtime'] as Map<String, dynamic>;
      expect(runtime['available'], isFalse);
      final spa = runtime['spa_stabilization'] as Map<String, dynamic>;
      expect(spa['bounded'], isTrue);
      final rSession = runtime['session'] as Map<String, dynamic>;
      expect(rSession['session_id'], session['session_id']);
      expect(rSession['continuation'], isTrue);
      final ir = env['browser_ir'] as Map<String, dynamic>;
      expect(ir['runtime_identity'], isA<String>());
      expect(env['unified_runtime_graph'], isA<Map>());
      expect(env['pipeline_hash'], isA<String>());
      expect(env['global_runtime_fingerprint'], isA<String>());
    });

    test('extractWithSession tick changes pipeline_hash', () async {
      final session = createRuntimeSession();
      final t0 =
          await extractWithSession('ftp://wwx.invalid/c', session, tick: 0);
      final t1 =
          await extractWithSession('ftp://wwx.invalid/c', session, tick: 1);
      expect(t0['pipeline_hash'], isNot(t1['pipeline_hash']));
    });

    test('continueAuthenticatedRuntime restores session from disk', () async {
      final tmp = Directory.systemTemp.createTempSync('wwx_cont_');
      try {
        final path = '${tmp.path}/cont.enc';
        final session = createRuntimeSession(<String, dynamic>{
          'cookies': <dynamic>['ck'],
        });
        persistRuntimeSession(path, session, 'ck-key');

        final env = await continueAuthenticatedRuntime(
          'ftp://wwx.invalid/c',
          sessionPath: path,
          encryptionKey: 'ck-key',
          tick: 7,
        );
        expect(env['bounded'], isTrue);
        final runtime = env['runtime'] as Map<String, dynamic>;
        final rSession = runtime['session'] as Map<String, dynamic>;
        // session_id derived from restored session
        expect(rSession['session_id'], isA<String>());
        expect(rSession['continuation'], isTrue);
        expect(env['pipeline_hash'], isA<String>());
      } finally {
        tmp.deleteSync(recursive: true);
      }
    });
  });
}
