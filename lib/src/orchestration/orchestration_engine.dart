Map<String, dynamic> orchestrate(String seed) => {
      'seed': seed,
      'plan': {
        'steps': ['ingest', 'extract', 'graph'],
        'bounded': true
      },
      'bounded': true,
    };
