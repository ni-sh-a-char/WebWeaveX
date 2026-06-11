/// Port of the core.application cognition closure —
/// `run_application_cognition` and its 12 engines, over the certified
/// bs4-parity soup. Proven Python ≡ JavaScript ≡ Dart by execution
/// (validation/semantic_ir/).
library;

import '../semantic_ir/py_compat.dart';
import '../soup/soup.dart';
import 'runtime_application.dart' show executeRuntimeObjective;

const int _maxItems = 1000;
const int _maxForms = 500;
const int _maxNav = 500;
const int _maxWidgets = 1000;

String _cap(String s, int n) => s.length > n ? s.substring(0, n) : s;

List<T> _capList<T>(List<T> xs, int n) =>
    xs.length > n ? xs.sublist(0, n) : xs;

String _attr(SoupTag tag, String key, [String dflt = '']) {
  final v = tag.attrs.containsKey(key) ? tag.attrs[key] : dflt;
  if (v is List) return v.join(' ');
  return pyToStr(v);
}

/// bs4 find_all(attrs={key: value}): attribute equality on the
/// space-joined value.
List<SoupTag> _findAllByAttr(SoupTag root, String key, String value,
    {int? limit}) {
  final out = <SoupTag>[];
  for (final tag in root.findAll(null)) {
    if (tag.attrs.containsKey(key) && _attr(tag, key) == value) {
      out.add(tag);
      if (limit != null && out.length >= limit) break;
    }
  }
  return out;
}

/// bs4 find_all(class_=...): the matcher runs against EACH class token.
List<SoupTag> _findAllByClass(SoupTag root, bool Function(String) matches,
    {int? limit}) {
  final out = <SoupTag>[];
  for (final tag in root.findAll(null)) {
    final cls = tag.attrs['class'];
    if (cls is List && cls.any((c) => matches(c as String))) {
      out.add(tag);
      if (limit != null && out.length >= limit) break;
    }
  }
  return out;
}

/// Port of core.application.ui_semantic_engine.extract_ui_semantics.
Map<String, dynamic> extractUiSemantics(String? html) {
  final soup = Soup(html ?? '');
  final semantics = <String, List<Map<String, dynamic>>>{
    'dashboards': [],
    'forms': [],
    'navigation_menus': [],
    'tables': [],
    'charts': [],
    'filters': [],
    'search_bars': [],
    'sidebars': [],
    'tabs': [],
  };

  for (final form in _capList(soup.findAll('form'), _maxItems)) {
    semantics['forms']!.add(<String, dynamic>{
      'action': _cap(_attr(form, 'action'), 500),
      'id': _cap(_attr(form, 'id'), 200),
    });
  }
  for (final nav
      in _capList(soup.findAll(const ['nav', 'header']), _maxItems)) {
    semantics['navigation_menus']!.add(<String, dynamic>{
      'tag': nav.name,
      'links': nav.findAll('a').length,
    });
  }
  for (final table in _capList(soup.findAll('table'), _maxItems)) {
    semantics['tables']!
        .add(<String, dynamic>{'rows': table.findAll('tr').length});
  }
  if (RegExp(r'dashboard|metrics|kpi', caseSensitive: false)
      .hasMatch(html ?? '')) {
    semantics['dashboards']!.add(<String, dynamic>{'detected': true});
  }
  for (final _ in _capList(soup.findAll('canvas'), _maxItems)) {
    semantics['charts']!.add(<String, dynamic>{'type': 'canvas'});
  }
  for (final node
      in _capList(soup.findAll(const ['input', 'select']), _maxItems)) {
    final nodeType = _attr(node, 'type').toLowerCase();
    final name = _attr(node, 'name');
    if (const {'search', 'text'}.contains(nodeType) &&
        name.toLowerCase().contains('search')) {
      semantics['search_bars']!
          .add(<String, dynamic>{'name': _cap(name, 200)});
    } else if (const {'select', 'checkbox', 'radio'}.contains(nodeType)) {
      semantics['filters']!.add(<String, dynamic>{
        'type': nodeType,
        'name': _cap(name, 200),
      });
    }
  }
  for (final _ in _capList(soup.findAll('aside'), _maxItems)) {
    semantics['sidebars']!.add(<String, dynamic>{'tag': 'aside'});
  }
  for (final tab
      in _capList(_findAllByAttr(soup, 'role', 'tab'), _maxItems)) {
    semantics['tabs']!.add(<String, dynamic>{
      'label': _cap(tab.getText(strip: true), 200),
    });
  }

  return <String, dynamic>{'semantics': semantics, 'bounded': true};
}

/// Port of core.application.form_runtime_engine.build_form_runtime.
Map<String, dynamic> buildFormRuntime(String? html) {
  final soup = Soup(html ?? '');
  final forms = <Map<String, dynamic>>[];

  for (final form in _capList(soup.findAll('form'), _maxForms)) {
    final inputs = <Map<String, dynamic>>[
      for (final field
          in form.findAll(const ['input', 'select', 'textarea']))
        <String, dynamic>{
          'name': _cap(_attr(field, 'name'), 200),
          'type': _cap(
              field.attrs.containsKey('type')
                  ? _attr(field, 'type')
                  : field.name,
              50),
          'required': field.attrs.containsKey('required'),
        }
    ];
    final csrfFields = <dynamic>[
      for (final inp in form.findAll('input'))
        if (_attr(inp, 'name').toLowerCase().contains('csrf'))
          inp.attrs.containsKey('name') ? _attr(inp, 'name') : ''
    ]..sort((a, b) => pyToStr(a).compareTo(pyToStr(b)));

    forms.add(<String, dynamic>{
      'action': _cap(_attr(form, 'action'), 500),
      'inputs': pyStableSortedBy(inputs, (m) => m['name'] as String),
      'csrf_fields': csrfFields,
      'multi_step': form.findAll('fieldset').length > 1,
      'bounded': true,
    });
  }

  return <String, dynamic>{
    'forms': forms,
    'form_count': forms.length,
    'bounded': true,
  };
}

/// Port of core.application.dashboard_runtime_engine.build_dashboard_runtime.
Map<String, dynamic> buildDashboardRuntime(String? html) {
  final soup = Soup(html ?? '');
  final widgetRe = RegExp(r'widget|card|metric|kpi', caseSensitive: false);
  final widgets = <Map<String, dynamic>>[
    for (final node in _capList(
        _findAllByClass(soup, widgetRe.hasMatch), _maxWidgets))
      <String, dynamic>{
        'text': _cap(node.getText(strip: true), 500),
        'tag': node.name,
      }
  ];
  final tables = <Map<String, dynamic>>[
    for (final table in _capList(soup.findAll('table'), _maxWidgets))
      <String, dynamic>{
        'rows': table.findAll('tr').length,
        'columns': table.findAll('th').length,
      }
  ];
  final filters = <Map<String, dynamic>>[
    for (final select in _capList(soup.findAll('select'), _maxWidgets))
      <String, dynamic>{'name': _cap(_attr(select, 'name'), 200)}
  ];
  final charts = <Map<String, dynamic>>[
    for (final canvas in _capList(soup.findAll('canvas'), _maxWidgets))
      <String, dynamic>{
        'type': 'canvas',
        'live': canvas.attrs.containsKey('data-live'),
      }
  ];
  return <String, dynamic>{
    'widgets': widgets,
    'metrics': <Map<String, dynamic>>[
      for (final w in widgets)
        if (pyTruthy(w['text'])) w
    ],
    'tables': tables,
    'filters': filters,
    'charts': charts,
    'update_interval': 30,
    'bounded': true,
  };
}

/// Port of core.application.navigation_semantic_engine
/// .build_navigation_semantics.
Map<String, dynamic> buildNavigationSemantics(String? html, String route,
    [List<dynamic>? routeHistory]) {
  final soup = Soup(html ?? '');
  final menus = <Map<String, dynamic>>[];
  for (final nav in _capList(soup.findAll('nav'), _maxNav)) {
    for (final link in nav.findAll('a')) {
      final href = _cap(_attr(link, 'href'), 500);
      if (pyTruthy(href)) {
        menus.add(<String, dynamic>{
          'href': href,
          'text': _cap(link.getText(strip: true), 200),
        });
      }
    }
  }
  final breadcrumbs = <String>[
    for (final crumb in _capList(
        _findAllByClass(soup, (c) => c.contains('breadcrumb')), _maxNav))
      _cap(crumb.getText(strip: true), 500)
  ];
  var routes = <dynamic>[
    <String, dynamic>{'path': route, 'order': 0}
  ];
  if (pyTruthy(routeHistory)) {
    routes = _capList(List<dynamic>.from(routeHistory!), _maxNav);
  }
  final tabs = <Map<String, dynamic>>[
    for (final tab in _capList(_findAllByAttr(soup, 'role', 'tab'), _maxNav))
      <String, dynamic>{'label': _cap(tab.getText(strip: true), 200)}
  ];
  return <String, dynamic>{
    'menus':
        pyStableSortedBy(menus, (m) => pyToStr(pyGet(m, 'href', ''))),
    'breadcrumbs': breadcrumbs,
    'routes': routes,
    'spa_transitions': routes.length > 1,
    'tab_hierarchy': tabs,
    'bounded': true,
  };
}

/// Port of core.application.application_state_engine.build_application_state.
Map<String, dynamic> buildApplicationState(String route,
    [List<dynamic>? forms,
    List<dynamic>? modals,
    List<dynamic>? widgets,
    List<dynamic>? tabs,
    bool authenticated = false,
    Map<dynamic, dynamic>? runtimeState]) {
  return <String, dynamic>{
    'route': _cap(route, 2000),
    'forms': _capList(List<dynamic>.from(forms ?? const <dynamic>[]), 500),
    'modals': _capList(List<dynamic>.from(modals ?? const <dynamic>[]), 200),
    'widgets':
        _capList(List<dynamic>.from(widgets ?? const <dynamic>[]), 1000),
    'tabs': _capList(List<dynamic>.from(tabs ?? const <dynamic>[]), 100),
    'authenticated': authenticated,
    'runtime_state':
        Map<dynamic, dynamic>.from(runtimeState ?? const <dynamic, dynamic>{}),
    'bounded': true,
  };
}

/// Port of core.application.application_transition_engine
/// .build_application_transitions.
List<Map<String, dynamic>> buildApplicationTransitions(List<dynamic> states) {
  final transitions = <Map<String, dynamic>>[
    for (var i = 0; i < states.length - 1; i++)
      <String, dynamic>{
        'from': pyToStr(pyGet(states[i] as Map, 'route', '')),
        'to': pyToStr(pyGet(states[i + 1] as Map, 'route', '')),
        'relation': 'transition',
        'order': i,
      }
  ];
  return _capList(transitions, 10000);
}

/// Port of core.application.action_graph_engine.build_action_graph.
Map<String, dynamic> buildActionGraph(List<dynamic> interactions) {
  final nodes = <Map<String, dynamic>>[];
  final edges = <Map<String, dynamic>>[];
  final bounded = _capList(interactions, 10000);
  for (var index = 0; index < bounded.length; index++) {
    final action = bounded[index] as Map;
    final actionType = pyToStr(
        pyGet(action, 'action', pyGet(action, 'type', 'action')));
    final selector = pyToStr(pyGet(action, 'selector', ''));
    final nodeId = 'action_$index';
    nodes.add(<String, dynamic>{
      'id': nodeId,
      'type': actionType,
      'selector': selector,
    });
    if (index > 0) {
      edges.add(<String, dynamic>{
        'from': 'action_${index - 1}',
        'to': nodeId,
        'relation': 'sequential',
      });
    }
  }
  return <String, dynamic>{'nodes': nodes, 'edges': edges, 'bounded': true};
}

/// Port of core.application.workflow_graph_engine.build_workflow_graph.
Map<String, dynamic> buildWorkflowGraph(List<dynamic> states,
    List<dynamic> transitions, List<dynamic> actions) {
  final nodes = <Map<String, dynamic>>[];
  final boundedStates = _capList(states, 5000);
  for (var index = 0; index < boundedStates.length; index++) {
    final route =
        pyToStr(pyGet(boundedStates[index] as Map, 'route', 'state_$index'));
    nodes.add(<String, dynamic>{'id': route, 'type': 'page'});
  }
  final edges = <Map<String, dynamic>>[];
  for (final transition in _capList(transitions, 10000)) {
    edges.add(<String, dynamic>{
      'from': pyToStr(pyGet(transition as Map, 'from', '')),
      'to': pyToStr(pyGet(transition, 'to', '')),
      'relation': pyToStr(pyGet(transition, 'relation', 'transition')),
    });
  }
  for (final action in _capList(actions, 10000)) {
    final actionType =
        pyToStr(pyGet(action as Map, 'action', pyGet(action, 'type', '')));
    var relation = 'submit';
    if (actionType == 'click') {
      relation = 'navigate';
    } else if (actionType.contains('modal')) {
      relation = 'open_modal';
    }
    edges.add(<String, dynamic>{
      'from': pyToStr(pyGet(action, 'from', '')),
      'to': pyToStr(pyGet(action, 'to', '')),
      'relation': relation,
    });
  }
  return <String, dynamic>{
    'nodes': pyStableSortedBy(nodes, (n) => n['id'] as String),
    'edges': pyStableSortedBy(
        edges,
        (e) =>
            '${pyGet(e, 'from', '')}\u0000${pyGet(e, 'to', '')}\u0000${pyGet(e, 'relation', '')}'),
    'bounded': true,
  };
}

const Map<String, String> _intentMap = {
  'extract_dashboard': 'observe_metrics',
  'login': 'authenticate',
  'export_report': 'export_data',
  'extract_invoices': 'collect_records',
  'monitor_metrics': 'continuous_observe',
};

/// Port of core.application.application_intent_engine
/// .resolve_application_intent.
Map<String, dynamic> resolveApplicationIntent(String objective) =>
    <String, dynamic>{
      'objective': objective,
      'intent': _intentMap[objective] ?? 'observe',
      'bounded': true,
    };

/// Port of core.application.application_recovery_engine
/// .recover_application_runtime.
Map<String, dynamic> recoverApplicationRuntime(
    String? html, Map<dynamic, dynamic> state) {
  final forms = buildFormRuntime(html);
  final recoveredForms = <Map<dynamic, dynamic>>[];
  for (final form in pyGet(forms, 'forms', const <dynamic>[]) as List) {
    if (!pyTruthy(pyGet(form as Map, 'inputs', null))) {
      recoveredForms.add(<dynamic, dynamic>{
        ...form,
        'recovered': true,
        'inputs': <Map<String, dynamic>>[
          <String, dynamic>{
            'name': 'fallback',
            'type': 'text',
            'required': false
          }
        ],
      });
    } else {
      recoveredForms.add(<dynamic, dynamic>{...form, 'recovered': true});
    }
  }
  return <String, dynamic>{
    'route': pyGet(state, 'route', '/'),
    'forms_recovered': recoveredForms,
    'modals_cleared':
        (pyGet(state, 'modals', const <dynamic>[]) as List).isEmpty,
    'session_valid': pyGet(state, 'authenticated', false),
    'workflow_resumed': true,
    'bounded': true,
  };
}

/// Port of core.application.application_context_engine
/// .build_application_context.
Map<String, dynamic> buildApplicationContext(
        String url, Map<dynamic, dynamic> state, Map<dynamic, dynamic> identity) =>
    <String, dynamic>{
      'url': url,
      'route': pyGet(state, 'route', url),
      'authenticated': pyGet(state, 'authenticated', false),
      'identity_profile': pyGet(identity, 'profile_id', 'default'),
      'bounded': true,
    };

/// Port of core.application.application_memory_engine
/// .remember_application_runtime.
Map<dynamic, dynamic> rememberApplicationRuntime(
    Map<dynamic, dynamic> memory, Map<dynamic, dynamic> update) {
  final merged = Map<dynamic, dynamic>.from(memory);
  for (final key in const [
    'workflows',
    'forms',
    'action_graphs',
    'navigation_flows',
    'dashboard_structures',
  ]) {
    merged.putIfAbsent(
        key, () => pyGet(update, key, pyGet(merged, key, <dynamic, dynamic>{})));
  }
  merged.addAll(update);
  merged['bounded'] = true;
  return merged;
}

/// Port of core.application.application_cognition_orchestrator
/// .run_application_cognition (keyword params become positionals in
/// declaration order).
Map<String, dynamic> runApplicationCognition(String url, String html,
    [List<dynamic>? interactions,
    Map<dynamic, dynamic>? memory,
    String objective = 'extract_dashboard',
    bool authenticated = false,
    Map<dynamic, dynamic>? identity,
    Map<dynamic, dynamic>? adaptiveRuntime,
    List<dynamic>? routeHistory,
    List<dynamic>? modals]) {
  final mem = Map<dynamic, dynamic>.from(memory ?? const <dynamic, dynamic>{});
  final acts = List<dynamic>.from(interactions ?? const <dynamic>[]);
  final ident = identity ?? <dynamic, dynamic>{};

  final ui = extractUiSemantics(html);
  final formsRuntime = buildFormRuntime(html);
  final dashboard = buildDashboardRuntime(html);
  final navigation = buildNavigationSemantics(html, url, routeHistory);

  final state = buildApplicationState(
      url,
      pyGet(formsRuntime, 'forms', const <dynamic>[]) as List,
      List<dynamic>.from(modals ?? const <dynamic>[]),
      pyGet(dashboard, 'widgets', const <dynamic>[]) as List,
      pyGet(navigation, 'tab_hierarchy', const <dynamic>[]) as List,
      authenticated);

  var states = <dynamic>[state];
  if (pyTruthy(pyGet(mem, 'application_state', null))) {
    states = <dynamic>[mem['application_state'], state];
  }

  final transitions = buildApplicationTransitions(states);
  final actionGraph = buildActionGraph(acts);
  final workflow = buildWorkflowGraph(states, transitions, acts);

  final intent = resolveApplicationIntent(objective);
  final execution = executeRuntimeObjective(
      objective,
      workflow,
      actionGraph,
      Map<String, dynamic>.from(navigation),
      adaptiveRuntime:
          adaptiveRuntime == null ? null : Map<String, dynamic>.from(adaptiveRuntime));

  final recovery = recoverApplicationRuntime(html, state);
  final context = buildApplicationContext(url, state, ident);

  final updatedMemory = rememberApplicationRuntime(mem, <dynamic, dynamic>{
    'application_state': state,
    'workflows': workflow,
    'forms': formsRuntime,
    'action_graphs': actionGraph,
    'navigation_flows': navigation,
    'dashboard_structures': dashboard,
    'objectives': <String>[objective],
    'ui_semantics': ui,
  });

  return <String, dynamic>{
    'application_state': state,
    'ui_semantics': ui,
    'forms': formsRuntime,
    'dashboard': dashboard,
    'navigation': navigation,
    'workflow': workflow,
    'action_graph': actionGraph,
    'intent': intent,
    'execution': execution,
    'recovery': recovery,
    'context': context,
    'memory': updatedMemory,
    'bounded': true,
  };
}
