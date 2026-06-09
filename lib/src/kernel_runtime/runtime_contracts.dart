/// Port of core/contracts/runtime_contracts.py — RuntimePhase + UniversalInput.
///
/// Parity contract: `UniversalInput(...).toDict()` is byte-identical to the
/// Python `UniversalInput(...).to_dict()` under `compute_deterministic_hash`.
library;

/// Canonical runtime phases (mirrors Python RuntimePhase enum values).
const List<String> runtimePhaseValues = <String>[
  'ingestion',
  'execution',
  'semantic',
  'causality',
  'synchronization',
  'memory',
  'reconstruction',
  'graph',
];

/// Canonical ingress descriptor for the runtime pipeline.
///
/// Mirrors the frozen Python dataclass `UniversalInput`: same fields, same
/// defaults, same `to_dict` shape (options sorted, session defaulted to `{}`,
/// `bounded: true` appended).
class UniversalInput {
  UniversalInput({
    required this.source,
    this.sourceType = 'auto',
    this.url = '',
    this.path = '',
    this.session,
    Map<String, dynamic>? options,
    this.tick = 0,
  }) : options = options ?? <String, dynamic>{};

  final String source;
  final String sourceType;
  final String url;
  final String path;
  final Map<String, dynamic>? session;
  final Map<String, dynamic> options;
  final int tick;

  /// Deterministic dict matching Python `UniversalInput.to_dict`.
  Map<String, dynamic> toDict() {
    final sortedOptions = <String, dynamic>{};
    final keys = options.keys.toList()..sort();
    for (final k in keys) {
      sortedOptions[k] = options[k];
    }
    return <String, dynamic>{
      'source': source,
      'source_type': sourceType,
      'url': url,
      'path': path,
      'session': session ?? <String, dynamic>{},
      'options': sortedOptions,
      'tick': tick,
      'bounded': true,
    };
  }
}
