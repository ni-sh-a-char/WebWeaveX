import 'dart:convert';
import 'dart:io';

import 'package:webweavex/src/adaptive/modal_recovery_engine.dart';
import 'package:webweavex/src/crypto/hashing.dart';
import 'package:webweavex/src/ingestion/universal_ingestion_engine.dart';
import 'package:webweavex/src/interaction/pagination_engine.dart';
import 'package:webweavex/src/multimodal/universal_multimodal_extraction_engine.dart';

void main() {
  final page1 = <String, dynamic>{
    'url': 'https://x.test/1',
    '_test_url': 'https://x.test/1',
  };
  final pageChain = <String, dynamic>{
    'url': 'https://l.test/a',
    '_test_url': 'https://l.test/a',
    '_test_paginate': (String cur) =>
        {
          'https://l.test/a': 'https://l.test/b',
          'https://l.test/b': 'https://l.test/c',
        }[cur] ??
        '',
  };
  final out = {
    'paginated_none':
        computeDeterministicHash(extractPaginatedContent(null, '.next')),
    'paginated_basic':
        computeDeterministicHash(extractPaginatedContent(page1, '.next')),
    'paginated_chain':
        computeDeterministicHash(extractPaginatedContent(pageChain, '.next')),
    'modal_none': computeDeterministicHash(recoverModalRuntime(null)),
    'modal_html': computeDeterministicHash(recoverModalRuntime(null,
        html: "<div class='modal'><button class='close'>x</button></div>")),
    'ingest_missing':
        computeDeterministicHash(ingestInput(r'C:\nonexistent\file.html')),
    'multimodal_missing': computeDeterministicHash(
        extractMultimodal(r'C:\nonexistent\img.png')),
  };
  stdout.write(const JsonEncoder.withIndent(' ').convert(
      Map.fromEntries(out.entries.toList()..sort((a, b) => a.key.compareTo(b.key)))));
}
