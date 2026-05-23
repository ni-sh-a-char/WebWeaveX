import '../crypto/kaalka_runtime.dart';
import '../determinism/dom_stabilization.dart';

Map<String, dynamic> stabilizeSpaDom(String html, {String route = '/'}) {
  final stabilized = stabilizeDomHtml(html);
  final stableDomHash = computeStableDomHash(html);
  final spaFingerprint = computeSpaFingerprint(html);
  String? framework;
  if (RegExp(r'data-reactroot|__REACT', caseSensitive: false).hasMatch(html)) {
    framework = 'react';
  } else if (RegExp(r'data-v-', caseSensitive: false).hasMatch(html)) {
    framework = 'vue';
  } else if (RegExp(r'ng-version|_ngcontent', caseSensitive: false).hasMatch(html)) {
    framework = 'angular';
  }
  return {
    'framework': framework,
    'stabilized_html': stabilized,
    'stable_dom_hash': stableDomHash,
    'spa_fingerprint': spaFingerprint,
    'route_hash': computeDeterministicHash({'route': route, 'stable_dom_hash': stableDomHash}),
    'bounded': true,
  };
}
