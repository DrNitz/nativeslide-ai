"""
NativeSlide AI — PDF Extraction Service
Handles PDF upload validation, text extraction, and content preprocessing.
"""
from __future__ import annotations

import io
import re
from fastapi import HTTPException, UploadFile, status

# Try pdfplumber first, fallback to pypdf
try:
    import pdfplumber  # type: ignore
    _HAS_PDFPLUMBER = True
except ImportError:
    _HAS_PDFPLUMBER = False

try:
    import pypdf  # type: ignore
    _HAS_PYPDF = True
except ImportError:
    _HAS_PYPDF = False


class PDFService:
    """Validates and extracts clean, structured text from uploaded PDF files."""

    MAX_FILE_SIZE_BYTES = 25 * 1024 * 1024  # 25 MB

    async def validate_and_extract(self, file: UploadFile) -> str:
        """
        Validate file size and content type, then extract all readable text.
        Returns cleaned, normalized text string.
        """
        if not file.filename or not file.filename.lower().endswith(".pdf"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only PDF documents are supported (.pdf).",
            )

        content = await file.read()
        if len(content) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Uploaded file is empty.",
            )

        if len(content) > self.MAX_FILE_SIZE_BYTES:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"File exceeds maximum allowed size of {self.MAX_FILE_SIZE_BYTES // (1024*1024)} MB.",
            )

        extracted_text = self._extract_text_from_bytes(content)
        if not extracted_text.strip():
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="No readable text could be extracted from this PDF. It may be scanned or image-only.",
            )

        return self._clean_text(extracted_text)

    def _extract_text_from_bytes(self, content: bytes) -> str:
        """Extract text using pdfplumber or pypdf."""
        pages_text: list[str] = []

        if _HAS_PDFPLUMBER:
            try:
                with pdfplumber.open(io.BytesIO(content)) as pdf:
                    for page in pdf.pages:
                        t = page.extract_text()
                        if t:
                            pages_text.append(t)
                if pages_text:
                    return "\n\n".join(pages_text)
            except Exception:
                pass  # Fall back to pypdf

        if _HAS_PYPDF:
            try:
                reader = pypdf.PdfReader(io.BytesIO(content))
                for page in reader.pages:
                    t = page.extract_text()
                    if t:
                        pages_text.append(t)
                return "\n\n".join(pages_text)
            except Exception as exc:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=f"Failed to parse PDF file: {exc}",
                )

        # Fallback if neither library is installed
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="PDF extraction libraries (pdfplumber/pypdf) are not installed.",
        )

    def _clean_text(self, raw: str) -> str:
        """Clean extracted PDF text: strip headers, footers, page numbers, duplicate spaces."""
        lines = raw.splitlines()
        cleaned_lines: list[str] = []

        # Patterns for page numbers like "Page 1 of 12", "1 / 45", "- 3 -"
        page_pattern = re.compile(
            r"^(page\s+\d+(\s+of\s+\d+)?|\d+\s*/\s*\d+|[-–—]\s*\d+\s*[-–—]|\d+)$",
            re.IGNORECASE,
        )

        for line in lines:
            trimmed = line.strip()
            # Ignore empty lines
            if not trimmed:
                continue
            # Ignore page numbers
            if page_pattern.match(trimmed):
                continue
            # Normalize internal spaces
            normalized = re.sub(r"\s+", " ", trimmed)
            cleaned_lines.append(normalized)

        return "\n\n".join(cleaned_lines)
