import 'dart:collection';
import 'config.dart';

class Entity {
  final String type;
  final String value;

  Entity({required this.type, required this.value});

  Map<String, String> toMap() {
    return LinkedHashMap<String, String>.from({'type': type, 'value': value});
  }

  @override
  bool operator ==(Object other) {
    if (identical(this, other)) return true;
    return other is Entity && other.type == type && other.value == value;
  }

  @override
  int get hashCode => type.hashCode ^ value.hashCode;
}

class Entities {
  List<Entity> extract(String text) {
    if (text.isEmpty) return [];

    final entities = <Entity>[];
    final seen = <String>{};

    _extractPattern(text, Config.emailRegex, 'email', entities, seen);
    _extractPattern(text, Config.urlRegex, 'url', entities, seen);
    _extractPattern(text, Config.numberRegex, 'number', entities, seen);
    _extractPattern(text, Config.phoneRegex, 'phone', entities, seen);
    _extractPattern(
      text,
      Config.capitalizedRegex,
      'capitalized',
      entities,
      seen,
    );

    return entities;
  }

  void _extractPattern(
    String text,
    RegExp pattern,
    String type,
    List<Entity> entities,
    Set<String> seen,
  ) {
    for (final match in pattern.allMatches(text)) {
      final value = match.group(0)!;
      final key = '$type:$value';
      if (!seen.contains(key)) {
        seen.add(key);
        entities.add(Entity(type: type, value: value));
      }
    }
  }
}
