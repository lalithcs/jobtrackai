from __future__ import annotations

from typing import List

from .text_utils import tokenize


def resume_visual_impact_score(resume_text: str) -> float:
    lines: List[str] = resume_text.splitlines() or [resume_text]
    total_chars = max(len(resume_text), 1)
    whitespace_ratio = sum(1 for c in resume_text if c.isspace()) / total_chars

    bullets = sum(1 for line in lines if line.strip().startswith(("-", "*", "•")))
    heading_like = sum(1 for line in lines if line.strip().isupper() and len(line.strip()) > 2)

    tokens = tokenize(resume_text)
    unique_ratio = len(set(tokens)) / max(len(tokens), 1)

    # Heuristic weighted score (0..100)
    score = (
        30 * min(max(whitespace_ratio / 0.35, 0), 1)
        + 25 * min(bullets / 12, 1)
        + 20 * min(heading_like / 6, 1)
        + 25 * min(unique_ratio / 0.7, 1)
    )
    return round(min(max(score, 0), 100), 2)
