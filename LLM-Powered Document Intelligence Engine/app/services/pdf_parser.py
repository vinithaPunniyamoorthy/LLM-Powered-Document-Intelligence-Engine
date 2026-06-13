from pathlib import Path


def extract_text_from_file(path: str) -> str:
    suffix = Path(path).suffix.lower()

    if suffix == ".txt":
        return Path(path).read_text(encoding="utf-8")

    if suffix == ".pdf":
        try:
            import PyPDF2
        except ImportError as exc:
            raise RuntimeError("PyPDF2 is required for PDF parsing") from exc

        reader = PyPDF2.PdfReader(path)
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
        return text

    if suffix == ".docx":
        try:
            import docx
        except ImportError as exc:
            raise RuntimeError("python-docx is required for DOCX parsing") from exc

        document = docx.Document(path)
        return "\n".join(paragraph.text for paragraph in document.paragraphs)

    raise ValueError("Unsupported file format")
