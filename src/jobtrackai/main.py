from __future__ import annotations

from .interview import compute_interview_readiness
from .matching import match_candidate_to_job
from .models import CandidateProfile, InterviewDimensionScore, JobRole
from .skills import identify_skill_gaps

try:
    from fastapi import FastAPI
except ModuleNotFoundError:  # pragma: no cover
    FastAPI = None


if FastAPI is not None:
    app = FastAPI(title="JobTrackAI API", version="0.1.0")

    @app.get("/health")
    def health() -> dict:
        return {"status": "ok"}

    @app.post("/match")
    def match(candidate: CandidateProfile, job: JobRole):
        return match_candidate_to_job(candidate, job)

    @app.post("/interview/readiness")
    def interview_readiness(scores: InterviewDimensionScore):
        return compute_interview_readiness(scores)

    @app.post("/skills/gaps")
    def skill_gaps(candidate: CandidateProfile, job: JobRole):
        return identify_skill_gaps(candidate, job)
else:  # pragma: no cover
    app = None
