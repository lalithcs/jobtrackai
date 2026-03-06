from __future__ import annotations

from .fairness import institution_bias_adjustment
from .models import CandidateProfile, JobRole, MatchBreakdown, MatchResult
from .resume import resume_visual_impact_score
from .text_utils import cosine_similarity, jaccard_similarity


DEFAULT_WEIGHTS = {
    "skill_coverage": 0.35,
    "project_relevance": 0.20,
    "resume_quality": 0.20,
    "semantic_alignment": 0.25,
}


def _skill_coverage(candidate: CandidateProfile, job: JobRole) -> float:
    return 100.0 * jaccard_similarity(candidate.skills, job.required_skills)


def _project_relevance(candidate: CandidateProfile, job: JobRole) -> float:
    project_text = " ".join(candidate.projects)
    keyword_text = " ".join(job.preferred_projects_keywords)
    return 100.0 * cosine_similarity(project_text, keyword_text)


def _semantic_alignment(candidate: CandidateProfile, job: JobRole) -> float:
    profile_text = " ".join(candidate.skills + candidate.projects) + " " + candidate.resume_text
    job_text = " ".join(job.required_skills + job.preferred_projects_keywords) + " " + job.description
    return 100.0 * cosine_similarity(profile_text, job_text)


def match_candidate_to_job(candidate: CandidateProfile, job: JobRole) -> MatchResult:
    skill = _skill_coverage(candidate, job)
    proj = _project_relevance(candidate, job)
    resume = resume_visual_impact_score(candidate.resume_text)
    semantic = _semantic_alignment(candidate, job)

    raw = (
        DEFAULT_WEIGHTS["skill_coverage"] * skill
        + DEFAULT_WEIGHTS["project_relevance"] * proj
        + DEFAULT_WEIGHTS["resume_quality"] * resume
        + DEFAULT_WEIGHTS["semantic_alignment"] * semantic
    )

    adjusted, fairness_delta = institution_bias_adjustment(raw, candidate.institution_tier)

    breakdown = MatchBreakdown(
        skill_coverage=round(skill, 2),
        project_relevance=round(proj, 2),
        resume_quality=round(resume, 2),
        semantic_alignment=round(semantic, 2),
        fairness_adjustment=round(fairness_delta, 2),
    )

    explanation = [
        f"Skill coverage contributed {breakdown.skill_coverage:.2f}/100.",
        f"Project relevance contributed {breakdown.project_relevance:.2f}/100.",
        f"Resume visual impact contributed {breakdown.resume_quality:.2f}/100.",
        f"Semantic alignment contributed {breakdown.semantic_alignment:.2f}/100.",
    ]
    if fairness_delta:
        explanation.append(
            f"Fairness module applied a +{fairness_delta:.2f} uplift to reduce institutional bias."
        )

    return MatchResult(final_score=round(adjusted, 2), breakdown=breakdown, explanation=explanation)
