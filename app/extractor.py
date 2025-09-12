from typing import Tuple, Optional
import re
from PyPDF2 import PdfReader

ADDRESS_PATTERNS = [
    r'\b(?:carrera|cra|kra|cr|kr|calle|cll|cl|avenida|av|avda|ak|transversal|tv|trv|transv|diagonal|dg)\b\s*\d+[a-zA-Z]?\s*(?:#|nro|no|num|numero)?\s*\d+[a-zA-Z]?\s*-?\s*\d*',
]

def extract_text_from_pdf(path: str) -> str:
    reader = PdfReader(path)
    texts = []
    for page in reader.pages:
        texts.append(page.extract_text() or "")
    return "\n".join(texts)

def extract_text_from_txt(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()

def extract_text(path: str) -> str:
    if path.lower().endswith(".pdf"):
        return extract_text_from_pdf(path)
    return extract_text_from_txt(path)

def find_first_address(text: str) -> Optional[str]:
    t = text.lower()
    for pat in ADDRESS_PATTERNS:
        m = re.search(pat, t, re.IGNORECASE)
        if m:
            # devolver con la capitalización original aproximada (slice)
            start, end = m.span()
            return text[start:end].strip()
    return None

def extract_address(path: str) -> Tuple[Optional[str], str]:
    text = extract_text(path)
    addr = find_first_address(text) or None
    return addr, text
