from jobtrackai.interview import compute_interview_readiness
from jobtrackai.models import CandidateProfile, InterviewDimensionScore, JobRole
from jobtrackai.skills import identify_skill_gaps


def test_interview_readiness_weighted_score():
    scores = InterviewDimensionScore(
        concept_clarity=80,
        problem_solving=70,
        communication_confidence=90,
        code_correctness=75,
        time_efficiency=60,
    )
    readiness = compute_interview_readiness(scores)
    assert round(readiness.readiness_index, 2) == 75.75


def test_skill_gap_report_identifies_missing_skills():
    candidate = CandidateProfile(name="Dev", skills=["python", "git"])
    job = JobRole(title="ML Engineer", required_skills=["python", "pytorch", "mlops"])
    report = identify_skill_gaps(candidate, job)

    assert report.missing_skills == ["pytorch", "mlops"]
    assert "pytorch" in report.roadmap
