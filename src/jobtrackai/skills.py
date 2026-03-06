from __future__ import annotations

from typing import Dict, List

from .models import CandidateProfile, JobRole, SkillGapReport


def identify_skill_gaps(candidate: CandidateProfile, job: JobRole) -> SkillGapReport:
    existing = {s.lower() for s in candidate.skills}
    missing = [s for s in job.required_skills if s.lower() not in existing]

    roadmap: Dict[str, List[str]] = {
        skill: [
            f"Week 1: Learn {skill} fundamentals",
            f"Week 2: Build a mini-project using {skill}",
            f"Week 3: Solve interview-focused tasks on {skill}",
        ]
        for skill in missing
    }
    return SkillGapReport(missing_skills=missing, roadmap=roadmap)
