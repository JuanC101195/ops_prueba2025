from typing import List
import re

EQUIVALENCES = {
    "carrera": ["carrera", "cra", "kra", "cr", "kr"],
    "calle": ["calle", "cll", "cl"],
    "avenida": ["avenida", "av", "avda"],
    "avenida carrera": ["avenida carrera", "ak"],
    "transversal": ["transversal", "tv", "trv", "transv"],
    "diagonal": ["diagonal", "dg"],
}

NUM_EQ = ["#", "nro", "no", "num", "numero"]

def normalize_base(addr: str) -> str:
    s = addr.lower()
    s = re.sub(r"[.,;:]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s

def generate_homonyms(original: str) -> List[str]:
    s = normalize_base(original)

    # detectar tipo de vía
    via = None
    for canonical, variants in EQUIVALENCES.items():
        for v in variants:
            if re.search(rf"\b{re.escape(v)}\b", s):
                via = canonical
                break
        if via:
            break

    out = set()
    tokens = s.replace("-", " ").split()
    # reemplazos de numero
    base_variants = set()
    for ne in NUM_EQ:
        base_variants.add(s.replace("#", f" {ne} ").replace("  ", " "))
    base_variants.add(s.replace("#", " ").replace("  ", " "))

    for variant in base_variants:
        out.add(re.sub(r"\s+", " ", variant).strip())

    # expandir via
    if via:
        for v in EQUIVALENCES[via]:
            out.update({re.sub(r"\b" + via + r"\b", v, x) for x in list(out)})
            out.update({re.sub(r"\b" + v + r"\b", via, x) for x in list(out)})

    # versiones sin guiones y con espacios
    more = set()
    for x in list(out):
        more.add(x.replace("-", " "))
        more.add(x.replace(" - ", " "))
    out.update(more)

    # capitalización amigable
    pretty = {re.sub(r"\s+", " ", x).replace(" numero ", " Numero ").title().replace(" # ", " # ")
              for x in out}

    return sorted(pretty)
