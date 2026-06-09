import '../browser/browser_identity.dart';

Map<String, dynamic> reconstructBrowserState(Map<String, dynamic> extraction) {
  final identity = identityFromExtraction(extraction);
  final ir = extraction['browser_ir'] as Map? ?? {};
  return {
    'runtime_identity': identity['runtime_identity'],
    'tabs': [
      {'id': 'tab:0', 'path': '/'}
    ],
    'navigation_history': [
      {'path': '/', 'order': 0}
    ],
    'session': extraction['runtime']?['session'] ?? <String, dynamic>{},
    'storage': ir['storage'] ?? <String, dynamic>{},
    'bounded': true,
  };
}
