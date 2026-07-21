import 'package:test/test.dart';
import 'package:webweavex/webweavex.dart';

void main() {
  group('query engines', () {
    test('queryRuntimeGraph returns results for by_type query', () {
      final graph = {
        'nodes': [
          {'id': 'n1', 'type': 'file', 'name': 'test.dart'},
          {'id': 'n2', 'type': 'module', 'name': 'core'},
        ],
        'edges': [],
      };
      final result = queryRuntimeGraph(graph, {'query_type': 'by_type', 'type': 'file'});
      expect(result, isA<Map>());
      expect(result.containsKey('results'), isTrue);
      expect(result['count'], greaterThanOrEqualTo(1));
    });

    test('queryRuntimeGraph returns empty for non-matching type', () {
      final graph = {
        'nodes': [{'id': 'n1', 'type': 'file', 'name': 'test.dart'}],
        'edges': [],
      };
      final result = queryRuntimeGraph(graph, {'query_type': 'by_type', 'type': 'module'});
      expect(result['count'], equals(0));
    });

    test('queryRuntimeGraph handles empty graph', () {
      final graph = {'nodes': [], 'edges': []};
      final result = queryRuntimeGraph(graph, {'query_type': 'by_type', 'type': 'file'});
      expect(result['count'], equals(0));
    });
  });
}