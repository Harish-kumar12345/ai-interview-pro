import io
from typing import Any
import pypdf


def extract_resume_text(uploaded_file: Any) -> str:
    """Extract plain text from an uploaded PDF or text file."""
    if uploaded_file is None:
        return ""
    
    file_name = getattr(uploaded_file, "name", "").lower()
    
    # Text file
    if file_name.endswith(".txt"):
        try:
            return uploaded_file.getvalue().decode("utf-8", errors="ignore").strip()
        except Exception:
            return ""

    # PDF file
    if file_name.endswith(".pdf"):
        try:
            stream = io.BytesIO(uploaded_file.getvalue())
            reader = pypdf.PdfReader(stream)
            extracted_pages = []
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    extracted_pages.append(text)
            full_text = "\n".join(extracted_pages).strip()
            # Truncate to reasonable token limit (first ~3500 chars) to prevent context overflow
            return full_text[:3500]
        except Exception as exc:
            return f"[Error reading PDF: {exc}]"

    return ""

