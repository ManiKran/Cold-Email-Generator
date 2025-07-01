import pdfplumber
import docx
from fastapi import UploadFile

async def extract_text(upload_file: UploadFile) -> str:
    contents = await upload_file.read()
    filename = upload_file.filename

    if filename.endswith(".pdf"):
        return extract_pdf_text(contents)
    elif filename.endswith(".docx"):
        return extract_docx_text(contents)
    else:
        return "Unsupported file format"

def extract_pdf_text(contents: bytes) -> str:
    text = ""
    with pdfplumber.open(io.BytesIO(contents)) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text.strip()

def extract_docx_text(contents: bytes) -> str:
    doc = docx.Document(io.BytesIO(contents))
    return "\n".join([p.text for p in doc.paragraphs]).strip()

import io  # Required for in-memory file streams