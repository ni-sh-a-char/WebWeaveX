import '../determinism/dom_stabilization.dart';

bool replayDomEquivalent(String originalHtml, String replayedHtml) =>
    computeStableDomHash(originalHtml) == computeStableDomHash(replayedHtml);
