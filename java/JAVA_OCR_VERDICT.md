# JAVA_OCR_VERDICT

**Phase-4 audit (Session 28). Verdict: OCR-runtime REQUIRED — blocked.** Python canon `9625f4a`.
APIs: `extract_multimodal`, `ingest_input` (image branch), `universal_extract` (image/file branch).

## A. Concrete runtime
`extract_multimodal(path) → extract_ocr(path)`:
```
if pytesseract is None or Image is None: return {"available":False,"regions":[],"reason":"ocr_dependencies_missing",...}
if not Path(path).is_file():            return {"available":False,"regions":[],"reason":"file_not_found",...}
image = Image.open(path); ... pytesseract.image_to_data(image, output_type=DICT)  # native Tesseract
```
`ingest_input(path)` dispatches to `extract_multimodal` **only** for image extensions
(`.png/.jpg/.jpeg`); all other inputs are a pure dict (`detect_input_type` + `{path,input_type,
supported,bounded}`). `universal_extract` dispatches images→`extract_multimodal`, pdf→`extract_pdf_text`,
docx→`extract_docx_text`, etc.

## B. Observable output dependency
When OCR is available and the file exists, `regions` (text + bounding boxes + confidence) come from
`pytesseract.image_to_data` — i.e. the native Tesseract engine reading actual image pixels. `layout`,
`tables`, `forms`, `charts`, `ui`, and `multimodal_ir` are all derived from those OCR regions, so the
entire observable output is a function of the Tesseract result.

## C. Why Java cannot reproduce it (under project constraints)
The output is **environment-dependent, not just runtime-dependent**: a machine with Tesseract +
Pillow installed yields populated `regions`; a machine without yields the empty `ocr_dependencies_missing`
shape. There is no deterministic, dependency-free function here — the same `(api, input)` pair produces
different observable output on different machines. No pure-Java library reproduces a specific
Tesseract version's `image_to_data` byte-for-byte (OCR is model/version/locale dependent), and binding
native Tesseract via JNI would break the pure-Java/portable contract and re-introduce cross-platform
non-determinism. Byte-exact parity cannot be **guaranteed**.

## D. Why frontier reduction fails
The OCR `regions` are not a discarded intermediate — they are the root of every downstream field
(`layout`/`tables`/`forms`/`charts`/`ui`/`multimodal_ir`). The only OCR-free path is the degenerate
"dependencies missing / file not found" shape, which is not the API's behavior. There is no observable
surface that excludes the Tesseract result.

## Note on the portable sub-frontier
`detect_input_type` (suffix → type) and `ingest_input`'s non-image branches are pure and portable; but
the API contract spans image inputs, so `ingest_input`/`universal_extract` cannot be certified
byte-exact as a whole. They are blocked **via** the image/OCR branch, not because the non-image logic
is hard.

## Verdict
`extract_multimodal`, `ingest_input`, `universal_extract` = **OCR-runtime required (blocked)**.
Unblock lever: a deterministic OCR-result-injection contract (pass `regions`/`ocr` payload in), which
canon does not currently provide.
