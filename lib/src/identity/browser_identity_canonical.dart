/// Canonical Python-aligned `build_browser_identity(profile_id)` — Group C of
/// the Final Completion Protocol. Full port of the `core.identity.*` subsystem
/// (profile / user-agent / platform / language / timezone / webgl / canvas /
/// font / media-device / navigator engines + entropy + fingerprint), proven
/// Python ≡ JavaScript ≡ Dart by execution (validation/executable/).
///
/// `compute_kaalka_hash_payload` == `compute_kaalka_hash` == Dart
/// `computeDeterministicHash` (verified), so all payload hashes use it.
library;

import '../crypto/hashing.dart';

const List<String> _profileIds = <String>['default', 'profile_a', 'profile_b'];

const Map<String, String> _userAgents = <String, String>{
  'default': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
      'AppleWebKit/537.36 (KHTML, like Gecko) '
      'Chrome/120.0.0.0 Safari/537.36',
  'profile_a': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
      'AppleWebKit/537.36 (KHTML, like Gecko) '
      'Chrome/120.0.0.0 Safari/537.36',
  'profile_b': 'Mozilla/5.0 (X11; Linux x86_64) '
      'AppleWebKit/537.36 (KHTML, like Gecko) '
      'Chrome/120.0.0.0 Safari/537.36',
};

const Map<String, String> _platforms = <String, String>{
  'default': 'Win32',
  'profile_a': 'MacIntel',
  'profile_b': 'Linux x86_64',
};

const Map<String, List<String>> _languages = <String, List<String>>{
  'default': <String>['en-US', 'en'],
  'profile_a': <String>['en-GB', 'en'],
  'profile_b': <String>['en-US', 'en'],
};

const Map<String, String> _timezones = <String, String>{
  'default': 'America/New_York',
  'profile_a': 'Europe/London',
  'profile_b': 'America/Los_Angeles',
};

const Map<String, Map<String, dynamic>> _webgl = <String, Map<String, dynamic>>{
  'default': <String, dynamic>{
    'vendor': 'Google Inc. (Intel)',
    'renderer': 'ANGLE (Intel, Intel(R) UHD Graphics Direct3D11 vs_5_0 ps_5_0)',
    'extensions': <String>['WEBGL_debug_renderer_info', 'OES_texture_float'],
  },
  'profile_a': <String, dynamic>{
    'vendor': 'Apple Inc.',
    'renderer': 'Apple GPU',
    'extensions': <String>['WEBGL_debug_renderer_info'],
  },
  'profile_b': <String, dynamic>{
    'vendor': 'Google Inc. (NVIDIA)',
    'renderer': 'ANGLE (NVIDIA, NVIDIA GeForce GTX 1060)',
    'extensions': <String>[
      'WEBGL_debug_renderer_info',
      'EXT_texture_filter_anisotropic'
    ],
  },
};

const Map<String, List<String>> _fonts = <String, List<String>>{
  'default': <String>[
    'Arial',
    'Courier New',
    'Segoe UI',
    'Times New Roman',
    'Verdana'
  ],
  'profile_a': <String>['Arial', 'Helvetica', 'Menlo', 'Times New Roman'],
  'profile_b': <String>[
    'DejaVu Sans',
    'Liberation Sans',
    'Ubuntu',
    'Noto Sans'
  ],
};

const Map<String, Map<String, List<String>>> _devices =
    <String, Map<String, List<String>>>{
  'default': <String, List<String>>{
    'audio_inputs': <String>['Default Microphone'],
    'video_inputs': <String>['Integrated Camera'],
    'audio_outputs': <String>['Default Speakers'],
  },
  'profile_a': <String, List<String>>{
    'audio_inputs': <String>['MacBook Microphone'],
    'video_inputs': <String>['FaceTime HD Camera'],
    'audio_outputs': <String>['MacBook Speakers'],
  },
  'profile_b': <String, List<String>>{
    'audio_inputs': <String>['USB Audio Device'],
    'video_inputs': <String>['HD Pro Webcam'],
    'audio_outputs': <String>['HDMI Output'],
  },
};

const Map<String, Map<String, dynamic>> _screenProfiles =
    <String, Map<String, dynamic>>{
  'default': <String, dynamic>{'width': 1920, 'height': 1080, 'colorDepth': 24},
  'profile_a': <String, dynamic>{
    'width': 1440,
    'height': 900,
    'colorDepth': 24
  },
  'profile_b': <String, dynamic>{
    'width': 2560,
    'height': 1440,
    'colorDepth': 24
  },
};

String _bounded(String profileId) =>
    _profileIds.contains(profileId) ? profileId : 'default';

Map<String, dynamic> buildBrowserProfile([String profileId = 'default']) {
  final id = _bounded(profileId);
  return <String, dynamic>{
    'profile_id': id,
    'profile_seed': computeDeterministicHash(id),
    'rotation_index': 0,
    'bounded': true,
  };
}

Map<String, dynamic> buildUserAgentRuntime([String profileId = 'default']) =>
    <String, dynamic>{
      'user_agent': _userAgents[_bounded(profileId)],
      'bounded': true
    };

Map<String, dynamic> buildPlatformRuntime([String profileId = 'default']) =>
    <String, dynamic>{
      'platform': _platforms[_bounded(profileId)],
      'bounded': true
    };

Map<String, dynamic> buildLanguageRuntime([String profileId = 'default']) =>
    <String, dynamic>{
      'languages': List<String>.from(_languages[_bounded(profileId)]!),
      'bounded': true,
    };

Map<String, dynamic> buildTimezoneRuntime([String profileId = 'default']) =>
    <String, dynamic>{
      'timezone': _timezones[_bounded(profileId)],
      'bounded': true
    };

Map<String, dynamic> buildWebglRuntime([String profileId = 'default']) {
  final data = _webgl[_bounded(profileId)]!;
  return <String, dynamic>{
    'vendor': data['vendor'],
    'renderer': data['renderer'],
    'extensions': List<String>.from(data['extensions'] as List)..sort(),
    'bounded': true,
  };
}

Map<String, dynamic> buildCanvasRuntime([String profileId = 'default']) {
  final payload = <String, dynamic>{
    'profile_id': profileId,
    'canvas_seed': 'webweavex-canvas:$profileId',
  };
  return <String, dynamic>{
    'canvas_fingerprint': computeDeterministicHash(payload),
    'canvas_seed': payload['canvas_seed'],
    'bounded': true,
  };
}

Map<String, dynamic> buildFontRuntime([String profileId = 'default']) =>
    <String, dynamic>{
      'fonts': List<String>.from(_fonts[_bounded(profileId)]!)..sort(),
      'bounded': true,
    };

Map<String, dynamic> buildMediaDeviceRuntime([String profileId = 'default']) {
  final data = _devices[_bounded(profileId)]!;
  return <String, dynamic>{
    'audio_inputs': List<String>.from(data['audio_inputs']!),
    'video_inputs': List<String>.from(data['video_inputs']!),
    'audio_outputs': List<String>.from(data['audio_outputs']!),
    'bounded': true,
  };
}

Map<String, dynamic> buildNavigatorRuntime([String profileId = 'default']) {
  final ua = buildUserAgentRuntime(profileId);
  final platform = buildPlatformRuntime(profileId);
  final languages = buildLanguageRuntime(profileId);
  return <String, dynamic>{
    'webdriver': false,
    'plugins': <String>['Chrome PDF Plugin', 'Chrome PDF Viewer'],
    'mimeTypes': <String>['application/pdf'],
    'hardwareConcurrency': 8,
    'deviceMemory': 8,
    'languages': languages['languages'],
    'permissions': <String, dynamic>{
      'notifications': 'default',
      'geolocation': 'prompt',
    },
    'user_agent': ua['user_agent'],
    'platform': platform['platform'],
    'bounded': true,
  };
}

/// Port of core.identity.browser_entropy_engine.normalize_browser_fingerprint.
Map<String, dynamic> normalizeBrowserFingerprint(
    Map<String, dynamic> identity) {
  final normalized = <String, dynamic>{};
  final keys = identity.keys.toList()..sort();
  for (final key in keys) {
    if (key == 'bounded') continue;
    final value = identity[key];
    if (value is Map) {
      final inner = <String, dynamic>{};
      final ik = value.keys.map((dynamic k) => k.toString()).toList()..sort();
      for (final k in ik) {
        inner[k.toLowerCase()] = value[k];
      }
      normalized[key] = inner;
    } else if (value is List) {
      normalized[key] =
          value.map((dynamic e) => e.toString().toLowerCase()).toList()..sort();
    } else {
      normalized[key] = value.toString().trim().toLowerCase();
    }
  }
  return normalized;
}

String fingerprintBrowserIdentity(Map<String, dynamic> identity) =>
    computeDeterministicHash(normalizeBrowserFingerprint(identity));

Map<String, dynamic> computeRuntimeEntropy(Map<String, dynamic> identity) {
  final baseline =
      computeDeterministicHash(normalizeBrowserFingerprint(identity));
  return <String, dynamic>{
    'entropy_score': 0.0,
    'stable': true,
    'baseline_hash': baseline,
    'bounded': true,
  };
}

/// Port of webweavex.build_browser_identity(profile_id).
Map<String, dynamic> buildBrowserIdentity([String profileId = 'default']) {
  final profile = buildBrowserProfile(profileId);
  final boundedId = profile['profile_id'] as String;

  final ua = buildUserAgentRuntime(boundedId);
  final platform = buildPlatformRuntime(boundedId);
  final languages = buildLanguageRuntime(boundedId);
  final timezone = buildTimezoneRuntime(boundedId);
  final webgl = buildWebglRuntime(boundedId);
  final canvas = buildCanvasRuntime(boundedId);
  final fonts = buildFontRuntime(boundedId);
  final media = buildMediaDeviceRuntime(boundedId);
  final navigator = buildNavigatorRuntime(boundedId);

  final identity = <String, dynamic>{
    'profile_id': boundedId,
    'user_agent': ua['user_agent'],
    'platform': platform['platform'],
    'languages': languages['languages'],
    'timezone': timezone['timezone'],
    'screen': Map<String, dynamic>.from(
        _screenProfiles[boundedId] ?? _screenProfiles['default']!),
    'webgl': webgl,
    'fonts': fonts['fonts'],
    'media_devices': <String, dynamic>{
      'audio_inputs': media['audio_inputs'],
      'video_inputs': media['video_inputs'],
      'audio_outputs': media['audio_outputs'],
    },
    'canvas_fingerprint': canvas['canvas_fingerprint'],
    'navigator': navigator,
    'rotation_index': profile['rotation_index'] ?? 0,
    'bounded': true,
  };

  final entropy = computeRuntimeEntropy(identity);
  identity['entropy_profile'] = entropy['baseline_hash'];
  identity['fingerprint_hash'] = fingerprintBrowserIdentity(identity);
  return identity;
}
