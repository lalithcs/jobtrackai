from jobtrackai.matching import match_candidate_to_job
from jobtrackai.models import CandidateProfile, JobRole


def test_match_result_contains_explanation_and_valid_score():
    candidate = CandidateProfile(
        name="Asha",
        skills=["python", "fastapi", "sql"],
        projects=["Built an NLP resume analyzer with Python and transformers"],
        resume_text="""EXPERIENCE\n- Built APIs in FastAPI\n- Optimized SQL queries\nSKILLS\nPython SQL FastAPI""",
        institution_tier=3,
    )
    job = JobRole(
        title="Backend Engineer",
        required_skills=["python", "sql", "docker"],
        preferred_projects_keywords=["api", "backend", "nlp"],
        description="Build backend APIs and scalable data pipelines",
    )

    result = match_candidate_to_job(candidate, job)

    assert 0 <= result.final_score <= 100
    assert result.breakdown.skill_coverage >= 0
    assert len(result.explanation) >= 4
