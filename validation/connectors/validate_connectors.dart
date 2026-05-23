import 'package:webweavex/webweavex.dart';

void main() {
  final pg = extractPostgresRuntime({'tables': ['t']});
  final live = runLiveRuntime();
  if (pg['database_type'] != 'postgresql' || live['bounded'] != true) {
    throw StateError('connector validation failed');
  }
  print('PASS connectors');
}
