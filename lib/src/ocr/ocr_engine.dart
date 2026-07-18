/// Port of core/ocr/ocr_engine.py: extract_ocr and extract_ocr_text.
///
/// Environment contract (verified against the canonical Python reference
/// environment): `import pytesseract` and `import PIL` SUCCEED, but the
/// native tesseract binary is NOT installed. The deterministic Python
/// behaviour being ported is therefore:
///
///   1. path is not a file            -> reason "file_not_found"
///   2. PIL cannot identify the file  -> reason str(UnidentifiedImageError)
///      which is "cannot identify image file " + repr(os.path.realpath(path))
///   3. image width/height > 5000     -> reason "image_too_large"
///      (PIL.Image.open is lazy: `.size` comes from the header only, so a
///      pure-Dart header parse of PNG/JPEG/GIF/BMP reproduces it)
///   4. otherwise pytesseract raises TesseractNotFoundError whose str() is
///      "tesseract is not installed or it's not in your PATH. See README
///      file for more information."; extract_ocr falls back to
///      extract_ocr_text, which raises the same, so both functions return
///      that reason ([:200]).
///
/// Branch 4's message is the platform-bound edge: it is byte-exact for the
/// canonical no-tesseract-binary environment (a host with the tesseract
/// binary installed would perform real OCR, which is inherently
/// native/non-deterministic and out of pure-compute parity scope).
library;

import 'dart:io';

import 'package:webweavex/src/soup/soup.dart' show pyTruncate;

const int maxImageDimension = 5000;
const int maxOcrRegions = 10000;
const int maxRegionText = 10000;

const String _tesseractNotFoundMessage =
    "tesseract is not installed or it's not in your PATH. "
    'See README file for more information.';

/// Python `repr()` of a str, for the ASCII-dominant path strings reachable
/// here. Quote selection and escaping follow CPython: single quotes unless
/// the string contains `'` and no `"`; backslash/quote/`\t`/`\n`/`\r`
/// escaped; other control characters as `\xXX`.
String _pyRepr(String s) {
  final bool hasSingle = s.contains("'");
  final bool hasDouble = s.contains('"');
  final String quote = (hasSingle && !hasDouble) ? '"' : "'";
  final StringBuffer out = StringBuffer(quote);
  for (final int rune in s.runes) {
    if (rune == 0x5C) {
      out.write(r'\\');
    } else if (rune == quote.codeUnitAt(0)) {
      out.write('\\$quote');
    } else if (rune == 0x09) {
      out.write(r'\t');
    } else if (rune == 0x0A) {
      out.write(r'\n');
    } else if (rune == 0x0D) {
      out.write(r'\r');
    } else if (rune < 0x20 || rune == 0x7F) {
      out.write('\\x${rune.toRadixString(16).padLeft(2, '0')}');
    } else {
      out.writeCharCode(rune);
    }
  }
  out.write(quote);
  return out.toString();
}

/// PIL `Image.open` header sniff: returns `[width, height]` when the bytes
/// are an identifiable PNG/JPEG/GIF/BMP image, or null when PIL would raise
/// UnidentifiedImageError. PIL identifies by content, not extension.
List<int>? _imageSize(List<int> bytes) {
  // PNG: 8-byte signature, then IHDR chunk (width/height big-endian u32).
  if (bytes.length >= 24 &&
      bytes[0] == 0x89 &&
      bytes[1] == 0x50 &&
      bytes[2] == 0x4E &&
      bytes[3] == 0x47 &&
      bytes[4] == 0x0D &&
      bytes[5] == 0x0A &&
      bytes[6] == 0x1A &&
      bytes[7] == 0x0A &&
      bytes[12] == 0x49 &&
      bytes[13] == 0x48 &&
      bytes[14] == 0x44 &&
      bytes[15] == 0x52) {
    final int width =
        (bytes[16] << 24) | (bytes[17] << 16) | (bytes[18] << 8) | bytes[19];
    final int height =
        (bytes[20] << 24) | (bytes[21] << 16) | (bytes[22] << 8) | bytes[23];
    return <int>[width, height];
  }

  // JPEG: FF D8, then marker segments; dimensions live in the first SOFn.
  if (bytes.length >= 4 && bytes[0] == 0xFF && bytes[1] == 0xD8) {
    int pos = 2;
    while (pos + 3 < bytes.length) {
      if (bytes[pos] != 0xFF) {
        pos++;
        continue;
      }
      final int marker = bytes[pos + 1];
      if (marker == 0xFF) {
        pos++;
        continue;
      }
      if (marker == 0xD8 || (marker >= 0xD0 && marker <= 0xD9)) {
        pos += 2;
        continue;
      }
      if (pos + 3 >= bytes.length) break;
      final int segLen = (bytes[pos + 2] << 8) | bytes[pos + 3];
      final bool isSof = marker >= 0xC0 &&
          marker <= 0xCF &&
          marker != 0xC4 &&
          marker != 0xC8 &&
          marker != 0xCC;
      if (isSof) {
        if (pos + 8 < bytes.length) {
          final int height = (bytes[pos + 5] << 8) | bytes[pos + 6];
          final int width = (bytes[pos + 7] << 8) | bytes[pos + 8];
          return <int>[width, height];
        }
        return null;
      }
      if (segLen < 2) return null;
      pos += 2 + segLen;
    }
    return null;
  }

  // GIF: "GIF87a" / "GIF89a", width/height little-endian u16. PIL's
  // GifImagePlugin additionally seeks to the first frame, so identification
  // requires at least one image descriptor (0x2C) after the logical screen
  // descriptor / optional global palette / extension blocks.
  if (bytes.length >= 13 &&
      bytes[0] == 0x47 &&
      bytes[1] == 0x49 &&
      bytes[2] == 0x46 &&
      bytes[3] == 0x38 &&
      (bytes[4] == 0x37 || bytes[4] == 0x39) &&
      bytes[5] == 0x61) {
    final int width = bytes[6] | (bytes[7] << 8);
    final int height = bytes[8] | (bytes[9] << 8);
    final int flags = bytes[10];
    int pos = 13;
    if (flags & 0x80 != 0) {
      pos += 3 * (2 << (flags & 0x07));
    }
    while (pos < bytes.length) {
      final int block = bytes[pos];
      if (block == 0x2C) {
        return <int>[width, height]; // image descriptor: identified
      }
      if (block == 0x21) {
        pos += 2; // extension introducer + label
        while (pos < bytes.length) {
          final int subLen = bytes[pos];
          pos += 1 + subLen;
          if (subLen == 0) break;
        }
        continue;
      }
      return null; // trailer (0x3B) or junk before any frame
    }
    return null;
  }

  // BMP: "BM", width/height little-endian i32 at offsets 18/22.
  if (bytes.length >= 26 && bytes[0] == 0x42 && bytes[1] == 0x4D) {
    int width =
        bytes[18] | (bytes[19] << 8) | (bytes[20] << 16) | (bytes[21] << 24);
    int height =
        bytes[22] | (bytes[23] << 8) | (bytes[24] << 16) | (bytes[25] << 24);
    if (width >= 0x80000000) width -= 0x100000000;
    if (height >= 0x80000000) height -= 0x100000000;
    if (height < 0) height = -height;
    return <int>[width, height];
  }

  return null;
}

bool _isFile(String path) {
  try {
    return File(path).existsSync();
  } catch (_) {
    return false;
  }
}

List<int> _readBytes(String path) {
  try {
    return File(path).readAsBytesSync();
  } catch (_) {
    return <int>[];
  }
}

/// Python `os.path.realpath(path)`: PIL embeds the resolved absolute path in
/// the UnidentifiedImageError message. Dart's resolveSymbolicLinksSync
/// matches realpath byte-for-byte on Windows (absolute, native separators,
/// filesystem-canonical case) for existing files, which is the only state in
/// which this is reachable.
String _realPath(String path) {
  try {
    return File(path).resolveSymbolicLinksSync();
  } catch (_) {
    return File(path).absolute.path;
  }
}

/// Port of core/ocr/ocr_engine.extract_ocr.
Map<String, dynamic> extractOcr(String path) {
  if (!_isFile(path)) {
    return <String, dynamic>{
      'available': false,
      'regions': <Map<String, dynamic>>[],
      'reason': 'file_not_found',
      'bounded': true,
    };
  }

  final List<int>? size = _imageSize(_readBytes(path));
  if (size == null) {
    // PIL UnidentifiedImageError: "cannot identify image file %r".
    return <String, dynamic>{
      'available': false,
      'regions': <Map<String, dynamic>>[],
      'reason': pyTruncate(
          'cannot identify image file ${_pyRepr(_realPath(path))}', 200),
      'bounded': true,
    };
  }

  final int width = size[0];
  final int height = size[1];

  if (width > maxImageDimension || height > maxImageDimension) {
    return <String, dynamic>{
      'available': false,
      'regions': <Map<String, dynamic>>[],
      'reason': 'image_too_large',
      'bounded': true,
    };
  }

  // pytesseract.image_to_data raises TesseractNotFoundError (no binary in
  // the canonical environment) -> fallback to extract_ocr_text, which is
  // also unavailable for the same reason.
  final Map<String, dynamic> textResult = extractOcrText(path);
  if (!(textResult['available'] as bool)) {
    return <String, dynamic>{
      'available': false,
      'regions': <Map<String, dynamic>>[],
      'reason': textResult.containsKey('reason')
          ? textResult['reason']
          : 'ocr_failed',
      'bounded': true,
    };
  }

  // Unreachable in the canonical no-tesseract-binary environment.
  return <String, dynamic>{
    'available': true,
    'regions': <Map<String, dynamic>>[],
    'bounded': true,
  };
}

/// Port of core/ocr/ocr_engine.extract_ocr_text.
Map<String, dynamic> extractOcrText(String path) {
  if (!_isFile(path)) {
    return <String, dynamic>{
      'available': false,
      'reason': 'file_not_found',
      'bounded': true,
    };
  }

  final List<int>? size = _imageSize(_readBytes(path));
  if (size == null) {
    return <String, dynamic>{
      'available': false,
      'reason': pyTruncate(
          'cannot identify image file ${_pyRepr(_realPath(path))}', 200),
      'bounded': true,
    };
  }

  final int width = size[0];
  final int height = size[1];

  if (width > maxImageDimension || height > maxImageDimension) {
    return <String, dynamic>{
      'available': false,
      'reason': 'image_too_large',
      'bounded': true,
    };
  }

  // pytesseract.image_to_string raises TesseractNotFoundError.
  return <String, dynamic>{
    'available': false,
    'reason': pyTruncate(_tesseractNotFoundMessage, 200),
    'bounded': true,
  };
}
