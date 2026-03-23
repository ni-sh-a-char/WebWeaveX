class Cleaner {
  String clean(String text) {
    if (text.isEmpty) return '';
    return text.trim().replaceAll(RegExp(r'\s+'), ' ');
  }
}
