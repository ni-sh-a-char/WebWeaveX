/// WebWeaveX — deterministic runtime cognition infrastructure (Dart).
library webweavex;

export 'src/browser/authenticated_runtime.dart';
export 'src/browser/capture_runtime.dart';
export 'src/browser/extract_web.dart';
export 'src/browser/render_page.dart';
export 'src/crypto/kaalka_runtime.dart';
export 'src/determinism/dom_stabilization.dart';
export 'src/determinism/fingerprint.dart';
export 'src/determinism/normalization.dart';
export 'src/determinism/stable_serialize.dart';
export 'src/graph/runtime_graph.dart';
export 'src/kernel/runtime_pipeline.dart';
export 'src/memory/runtime_memory.dart';
export 'src/reconstruction/reconstruct_runtime.dart';
export 'src/replay/replay_equivalence.dart';

const version = '2.0.0';
