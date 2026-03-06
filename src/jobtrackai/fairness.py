from __future__ import annotations

from typing import Tuple


def institution_bias_adjustment(raw_score: float, institution_tier: int) -> Tuple[float, float]:
    """Normalize over-weighting of institution tier.

    tier 1 gets no change, tier 2 gets small uplift, tier 3 gets modest uplift
    to reduce institutional bias in early filtering.
    """
    uplift = {1: 0.0, 2: 2.0, 3: 4.0}.get(institution_tier, 0.0)
    adjusted = min(raw_score + uplift, 100.0)
    return adjusted, uplift
