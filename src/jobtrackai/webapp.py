from __future__ import annotations

import json
from dataclasses import asdict
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any, Dict

from .interview import compute_interview_readiness
from .matching import match_candidate_to_job
from .models import CandidateProfile, InterviewDimensionScore, JobRole
from .skills import identify_skill_gaps

HTML = """<!doctype html>
<html>
<head>
  <meta charset='utf-8' />
  <meta name='viewport' content='width=device-width,initial-scale=1' />
  <title>JobTrackAI Interface</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 2rem; background:#f6f8fb; color:#102a43; }
    .card { background:white; border-radius:12px; padding:1rem 1.25rem; margin-bottom:1rem; box-shadow:0 2px 10px rgba(16,42,67,0.08); }
    textarea, input { width:100%; margin:0.3rem 0 0.8rem; padding:0.5rem; }
    button { background:#2563eb; color:white; border:none; border-radius:8px; padding:0.55rem 1rem; cursor:pointer; }
    pre { background:#0b1020; color:#dbeafe; border-radius:8px; padding:0.8rem; overflow:auto; }
    .grid { display:grid; grid-template-columns:1fr 1fr; gap:1rem; }
  </style>
</head>
<body>
  <h1>JobTrackAI (Next-Gen) — Local Interface</h1>

  <div class='card'>
    <h2>1) Candidate ↔ Job Match</h2>
    <div class='grid'>
      <div>
        <label>Candidate Name</label><input id='name' value='Asha'/>
        <label>Skills (comma separated)</label><input id='skills' value='python,fastapi,sql'/>
        <label>Projects (comma separated)</label><input id='projects' value='Built an NLP resume analyzer,Created backend APIs'/>
        <label>Resume Text</label><textarea id='resume' rows='6'>EXPERIENCE\n- Built APIs in FastAPI\n- Optimized SQL queries\nSKILLS\nPython SQL FastAPI</textarea>
        <label>Institution Tier (1-3)</label><input id='tier' value='3'/>
      </div>
      <div>
        <label>Job Title</label><input id='title' value='Backend Engineer'/>
        <label>Required Skills (comma separated)</label><input id='required' value='python,sql,docker'/>
        <label>Preferred Project Keywords (comma separated)</label><input id='keywords' value='api,backend,nlp'/>
        <label>Job Description</label><textarea id='jd' rows='6'>Build backend APIs and scalable data pipelines.</textarea>
      </div>
    </div>
    <button onclick='runMatch()'>Run Match</button>
    <pre id='matchOut'>No result yet.</pre>
  </div>

  <div class='card'>
    <h2>2) Interview Readiness Index</h2>
    <label>Scores: concept,problem,communication,code,time</label>
    <input id='interview' value='80,70,90,75,60'/>
    <button onclick='runInterview()'>Compute Readiness</button>
    <pre id='interviewOut'>No result yet.</pre>
  </div>

  <div class='card'>
    <h2>3) Skill Gap Roadmap</h2>
    <button onclick='runGaps()'>Generate Gaps</button>
    <pre id='gapOut'>No result yet.</pre>
  </div>

<script>
const csv = (v) => v.split(',').map(s => s.trim()).filter(Boolean)
const candidate = () => ({
  name: document.getElementById('name').value,
  skills: csv(document.getElementById('skills').value),
  projects: csv(document.getElementById('projects').value),
  resume_text: document.getElementById('resume').value,
  institution_tier: Number(document.getElementById('tier').value || 2),
})
const job = () => ({
  title: document.getElementById('title').value,
  required_skills: csv(document.getElementById('required').value),
  preferred_projects_keywords: csv(document.getElementById('keywords').value),
  description: document.getElementById('jd').value,
})
async function post(path, payload) {
  const r = await fetch(path, {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(payload)})
  return await r.json()
}
async function runMatch() {
  const data = await post('/api/match', {candidate: candidate(), job: job()})
  document.getElementById('matchOut').textContent = JSON.stringify(data, null, 2)
}
async function runInterview() {
  const [concept_clarity,problem_solving,communication_confidence,code_correctness,time_efficiency] = csv(document.getElementById('interview').value).map(Number)
  const data = await post('/api/interview/readiness', {concept_clarity,problem_solving,communication_confidence,code_correctness,time_efficiency})
  document.getElementById('interviewOut').textContent = JSON.stringify(data, null, 2)
}
async function runGaps() {
  const data = await post('/api/skills/gaps', {candidate: candidate(), job: job()})
  document.getElementById('gapOut').textContent = JSON.stringify(data, null, 2)
}
</script>
</body>
</html>"""


def _json_response(handler: BaseHTTPRequestHandler, payload: Dict[str, Any], status: int = 200) -> None:
    body = json.dumps(payload, indent=2).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


class JobTrackAIHandler(BaseHTTPRequestHandler):
    def _read_json(self) -> Dict[str, Any]:
        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length) if length > 0 else b"{}"
        return json.loads(raw.decode("utf-8") or "{}")

    def do_GET(self) -> None:  # noqa: N802
        if self.path in ("/", "/index.html"):
            body = HTML.encode("utf-8")
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        if self.path == "/health":
            _json_response(self, {"status": "ok"})
            return
        _json_response(self, {"error": "not found"}, status=404)

    def do_POST(self) -> None:  # noqa: N802
        try:
            payload = self._read_json()
            if self.path == "/api/match":
                candidate = CandidateProfile(**payload["candidate"])
                job = JobRole(**payload["job"])
                result = match_candidate_to_job(candidate, job)
                _json_response(self, asdict(result))
                return
            if self.path == "/api/interview/readiness":
                scores = InterviewDimensionScore(**payload)
                result = compute_interview_readiness(scores)
                _json_response(self, asdict(result))
                return
            if self.path == "/api/skills/gaps":
                candidate = CandidateProfile(**payload["candidate"])
                job = JobRole(**payload["job"])
                result = identify_skill_gaps(candidate, job)
                _json_response(self, asdict(result))
                return
            _json_response(self, {"error": "not found"}, status=404)
        except Exception as exc:  # broad by design for stable demo API
            _json_response(self, {"error": str(exc)}, status=400)


def run(host: str = "0.0.0.0", port: int = 8000) -> None:
    server = ThreadingHTTPServer((host, port), JobTrackAIHandler)
    print(f"JobTrackAI web interface running on http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run()
