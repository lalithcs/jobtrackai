# JobTrackAI (Next-Gen)

## 📌 Problem Statement
Despite possessing academic knowledge and project experience, many students fail to secure suitable job opportunities due to ineffective resume presentation, lack of interview readiness, and absence of personalized career guidance. Existing placement systems rely heavily on keyword-based filtering and opaque scoring mechanisms, offering limited explainability and actionable feedback. As a result, students receive repeated rejections without understanding skill gaps or improvement strategies, while recruiters face challenges in efficiently identifying industry-ready talent from large candidate pools.

Furthermore, current AI-based recruitment tools often function as black-box systems, where decision-making is entirely delegated to external models without transparent scoring logic, fairness controls, or measurable evaluation criteria. This raises concerns regarding explainability, bias, and academic contribution.

There is a need for an intelligent, explainable, and ethically responsible career guidance system that combines semantic intelligence with custom-designed matching algorithms, measurable resume evaluation, structured interview assessment, and bias-aware decision-making.

**JobTrackAI (Next-Gen)** addresses this gap by introducing a hybrid, AI-driven career readiness ecosystem that actively prepares students for industry expectations while supporting recruiters with transparent and data-driven talent selection.

## 🚀 Features of JobTrackAI (Next-Gen)

### 1) Hybrid Job Matching Algorithm (Core Contribution)
- Combines semantic similarity, rule-based scoring, and structured weighted computation.
- Final score integrates skill coverage, project relevance, resume quality, and semantic alignment.

### 2) Multimodal Resume Intelligence with Visual Impact Score
- Generates a quantified **Resume Visual Impact Score** from measurable structural and content heuristics.

### 3) Project-to-Skill Semantic Extraction
- Uses semantic signals in project text to improve role-fit analysis.

### 4) Explainable AI Job Matching
- Returns interpretable score breakdown and human-readable reasons for each match.

### 5) AI-Powered Resume Tailoring
- Foundation ready (can be extended with LLM rewriting pipeline).

### 6) Agentic AI Interviewer with Performance Scoring
- Computes an **Interview Readiness Index** using a structured scoring rubric.

### 7) Skill-Gap Identification & Learning Roadmaps
- Identifies missing skills and outputs short learning sprints.

### 8) Recruiter Talent Heatmap Dashboard
- API-ready data layer for cohort-level analytics.

### 9) Predictive Placement Analytics
- Architecture supports plugging in predictive probability models.

### 10) Ethics, Bias & Fairness Module
- Adds institution-tier normalization uplift to reduce systemic filtering bias.

### 11) Smart Outreach Automation
- Extensible module point for personalized outreach generation.

### 12) Proactive Career Alerts
- Extensible module point for recommendation + alert workflows.

## 🧩 Implemented MVP Components
- Hybrid matching engine with weighted scoring and explainable breakdown (`src/jobtrackai/matching.py`).
- Resume visual impact heuristic scorer (`src/jobtrackai/resume.py`).
- Bias-aware score normalization module (`src/jobtrackai/fairness.py`).
- Interview readiness scoring (`src/jobtrackai/interview.py`).
- Skill gap detection and roadmap generator (`src/jobtrackai/skills.py`).
- FastAPI endpoints for health, matching, interview readiness, and skill gaps (`src/jobtrackai/main.py`).

## ▶️ Run Locally (No External Dependencies)
```bash
python -m jobtrackai.webapp
```
Then open `http://localhost:8000`.

## ▶️ Optional FastAPI API
If you have network access for installing extras:
```bash
pip install -e .[api]
uvicorn jobtrackai.main:app --reload
```

## ✅ Run Tests
```bash
pytest -q
```
