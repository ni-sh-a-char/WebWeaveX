List<dynamic> queryMemoryHistory(Map<String, dynamic> mem) {
  final m = mem['memory'] as Map<String, dynamic>?;
  return (m?['runtime_history'] as List?) ?? [];
}
