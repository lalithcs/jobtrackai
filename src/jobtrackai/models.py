from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class CandidateProfile:
    name: str
    skills: List[str] = field(default_factory=list)
    projects: List[str] = field(default_factory=list)
    resume_text: str = ""
    institution_tier: int = 2


@dataclass
class JobRole:
    title: str
    required_skills: List[str] = field(default_factory=list)
    preferred_projects_keywords: List[str] = field(default_factory=list)
    description: str = ""


@dataclass
class MatchBreakdown:
    skill_coverage: float
    project_relevance: float
    resume_quality: float
    semantic_alignment: float
    fairness_adjustment: float


@dataclass
class MatchResult:
    final_score: float
    breakdown: MatchBreakdown
    explanation: List[str]


@dataclass
class InterviewDimensionScore:
    concept_clarity: float
    problem_solving: float
    communication_confidence: float
    code_correctness: float
    time_efficiency: float


@dataclass
class InterviewReadiness:
    readiness_index: float
    dimensions: InterviewDimensionScore


@dataclass
class SkillGapReport:
    missing_skills: List[str]
    roadmap: Dict[str, List[str]]
