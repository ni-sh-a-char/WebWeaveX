from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

try:
    import pytesseract
    from PIL import Image
except Exception:
    pytesseract = None
    Image = None

MAX_IMAGE_DIMENSION = 5000
MAX_OCR_REGIONS = 10000
MAX_REGION_TEXT = 10_000


def extract_ocr(path: str) -> Dict[str, Any]:
    if pytesseract is None or Image is None:
        return {
            "available": False,
            "regions": [],
            "reason": "ocr_dependencies_missing",
            "bounded": True,
        }

    if not Path(path).is_file():
        return {
            "available": False,
            "regions": [],
            "reason": "file_not_found",
            "bounded": True,
        }

    try:
        image = Image.open(path)
    except Exception as exc:
        return {
            "available": False,
            "regions": [],
            "reason": str(exc)[:200],
            "bounded": True,
        }

    width, height = image.size

    if width > MAX_IMAGE_DIMENSION or height > MAX_IMAGE_DIMENSION:
        return {
            "available": False,
            "regions": [],
            "reason": "image_too_large",
            "bounded": True,
        }

    regions = []

    try:
        data = pytesseract.image_to_data(
            image,
            output_type=pytesseract.Output.DICT,
        )
        count = len(data.get("text", []))
        for idx in range(min(count, MAX_OCR_REGIONS)):
            text = str(data["text"][idx]).strip()
            if not text:
                continue
            regions.append({
                "bbox": [
                    int(data["left"][idx]),
                    int(data["top"][idx]),
                    int(data["width"][idx]),
                    int(data["height"][idx]),
                ],
                "text": text[:MAX_REGION_TEXT],
            })
    except Exception:
        text_result = extract_ocr_text(path)
        if not text_result.get("available"):
            return {
                "available": False,
                "regions": [],
                "reason": text_result.get("reason", "ocr_failed"),
                "bounded": True,
            }
        for line_idx, line in enumerate(
            text_result.get("text", "").splitlines()[:MAX_OCR_REGIONS]
        ):
            line = line.strip()
            if not line:
                continue
            regions.append({
                "bbox": [0, line_idx * 20, width, 20],
                "text": line[:MAX_REGION_TEXT],
            })

    return {
        "available": True,
        "regions": regions[:MAX_OCR_REGIONS],
        "bounded": True,
    }


def extract_ocr_text(path: str) -> Dict[str, Any]:
    if pytesseract is None or Image is None:
        return {
            "available": False,
            "reason": "ocr_dependencies_missing",
            "bounded": True,
        }

    if not Path(path).is_file():
        return {
            "available": False,
            "reason": "file_not_found",
            "bounded": True,
        }

    try:
        image = Image.open(path)
    except Exception as exc:
        return {
            "available": False,
            "reason": str(exc)[:200],
            "bounded": True,
        }

    width, height = image.size

    if width > MAX_IMAGE_DIMENSION or height > MAX_IMAGE_DIMENSION:
        return {
            "available": False,
            "reason": "image_too_large",
            "bounded": True,
        }

    try:
        text = pytesseract.image_to_string(image)
    except Exception as exc:
        return {
            "available": False,
            "reason": str(exc)[:200],
            "bounded": True,
        }

    return {
        "available": True,
        "text": text[:1_000_000],
        "bounded": True,
    }
