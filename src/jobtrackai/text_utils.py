from __future__ import annotations

import re
from collections import Counter
from math import sqrt
from typing import Iterable, List, Set

TOKEN_RE = re.compile(r"[a-zA-Z][a-zA-Z0-9+#.-]*")


def tokenize(text: str) -> List[str]:
    return [t.lower() for t in TOKEN_RE.findall(text)]


def jaccard_similarity(a: Iterable[str], b: Iterable[str]) -> float:
    set_a, set_b = set(a), set(b)
    if not set_a and not set_b:
        return 1.0
    if not set_a or not set_b:
        return 0.0
    return len(set_a & set_b) / len(set_a | set_b)


def cosine_similarity(a_text: str, b_text: str) -> float:
    a_tokens = tokenize(a_text)
    b_tokens = tokenize(b_text)
    if not a_tokens or not b_tokens:
        return 0.0
    ca, cb = Counter(a_tokens), Counter(b_tokens)
    vocab: Set[str] = set(ca) | set(cb)
    dot = sum(ca[t] * cb[t] for t in vocab)
    na = sqrt(sum(v * v for v in ca.values()))
    nb = sqrt(sum(v * v for v in cb.values()))
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)
