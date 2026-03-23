class Config {
  static final RegExp emailRegex = RegExp(
    r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
    caseSensitive: false,
  );

  static final RegExp urlRegex = RegExp(
    r'''https?://[^\s<>"']+''',
    caseSensitive: false,
  );

  static final RegExp numberRegex = RegExp(r'\b\d+(?:\.\d+)?\b');

  static final RegExp phoneRegex = RegExp(
    r'\+?\d{1,3}[-.\s]?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}',
  );

  static final RegExp capitalizedRegex = RegExp(
    r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b',
  );

  static const int chunkSize = 500;
  static const int chunkOverlap = 100;
}
