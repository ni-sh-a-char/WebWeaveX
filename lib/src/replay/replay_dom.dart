import '../determinism/dom_stabilization.dart';

Map<String, dynamic> replayDomSnapshot(String html) => {
      'stabilized': stabilizeDomHtml(html),
      'hash': computeStableDomHash(html),
      'bounded': true,
    };

bool validateDomReplayEquivalence(String a, String b) =>
    computeStableDomHash(a) == computeStableDomHash(b);
