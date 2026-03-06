from __future__ import annotations

from .models import InterviewDimensionScore, InterviewReadiness


def compute_interview_readiness(dim: InterviewDimensionScore) -> InterviewReadiness:
    readiness = (
        0.25 * dim.concept_clarity
        + 0.25 * dim.problem_solving
        + 0.15 * dim.communication_confidence
        + 0.25 * dim.code_correctness
        + 0.10 * dim.time_efficiency
    )
    return InterviewReadiness(readiness_index=round(readiness, 2), dimensions=dim)
