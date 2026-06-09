/// Port of core/execution/runtime_transition_engine.apply_runtime_transition.
const Map<String, List<String>> _validTransitions = <String, List<String>>{
  'idle': <String>['queued', 'simulating'],
  'queued': <String>['executing', 'rolled_back'],
  'executing': <String>['committed', 'rolled_back', 'failed'],
  'simulating': <String>['idle'],
  'committed': <String>['idle'],
  'rolled_back': <String>['idle'],
  'failed': <String>['recovering', 'idle'],
  'recovering': <String>['idle'],
};

Map<String, dynamic> applyRuntimeTransition(String state, String event) {
  final String current = _validTransitions.containsKey(state) ? state : 'idle';
  final List<String> targets = _validTransitions[current] ?? <String>['idle'];

  String nextState;
  if (event == 'enqueue' && targets.contains('queued')) {
    nextState = 'queued';
  } else if (event == 'execute' && targets.contains('executing')) {
    nextState = 'executing';
  } else if (event == 'commit' && targets.contains('committed')) {
    nextState = 'committed';
  } else if (event == 'rollback' && targets.contains('rolled_back')) {
    nextState = 'rolled_back';
  } else if (event == 'simulate' && targets.contains('simulating')) {
    nextState = 'simulating';
  } else if (event == 'fail' && targets.contains('failed')) {
    nextState = 'failed';
  } else if (event == 'recover' && targets.contains('recovering')) {
    nextState = 'recovering';
  } else {
    nextState = targets.isNotEmpty ? targets.first : 'idle';
  }

  return <String, dynamic>{
    'from': current,
    'to': nextState,
    'event': event,
    'valid': _validTransitions.containsKey(nextState),
    'bounded': true,
  };
}
