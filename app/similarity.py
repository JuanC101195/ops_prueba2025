import re
import unicodedata
from rapidfuzz import fuzz

_ABBREV_PATTERNS = [
    (r"\b(kra|kr|cr|cra)\b", "carrera"),
    (r"\b(cll|cl)\b", "calle"),
    (r"\b(av|avda|aven)\b", "avenida"),
    (r"\b(ak)\b", "avenida carrera"),
    (r"\b(tv|trv|transv)\b", "transversal"),
    (r"\b(dg)\b", "diagonal"),
    (r"\b(nro|no|num|número|numero)\b", "numero"),
]

def _strip_accents(s: str) -> str:
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")

def normalize(s: str) -> str:
    s = s.lower()
    s = _strip_accents(s)
    s = s.replace("-", " ")
    s = s.replace("/", " ")
    s = s.replace("#", " numero ")
    s = re.sub(r"[.,;:]", " ", s)
    for pat, repl in _ABBREV_PATTERNS:
        s = re.sub(pat, repl, s)
    s = re.sub(r"\s+", " ", s).strip()
    return s

def score(a: str, b: str) -> float:
    na, nb = normalize(a), normalize(b)
    return max(
        fuzz.token_set_ratio(na, nb),
        fuzz.token_sort_ratio(na, nb),
        fuzz.partial_ratio(na, nb),
    )

def is_similar(a: str, b: str, threshold: float = 90) -> bool:
    return score(a, b) >= threshold
