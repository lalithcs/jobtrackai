import json
import threading
import time
from urllib.request import Request, urlopen

from jobtrackai.webapp import JobTrackAIHandler, ThreadingHTTPServer


def test_webapp_health_and_match_endpoint():
    server = ThreadingHTTPServer(("127.0.0.1", 8765), JobTrackAIHandler)
    t = threading.Thread(target=server.serve_forever, daemon=True)
    t.start()
    time.sleep(0.05)

    with urlopen("http://127.0.0.1:8765/health") as resp:
        health = json.loads(resp.read().decode("utf-8"))
    assert health["status"] == "ok"

    payload = {
        "candidate": {
            "name": "Asha",
            "skills": ["python", "sql"],
            "projects": ["Built API backend"],
            "resume_text": "SKILLS\nPython SQL",
            "institution_tier": 2,
        },
        "job": {
            "title": "Backend Engineer",
            "required_skills": ["python", "docker"],
            "preferred_projects_keywords": ["api", "backend"],
            "description": "Build backend services",
        },
    }
    req = Request(
        "http://127.0.0.1:8765/api/match",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urlopen(req) as resp:
        result = json.loads(resp.read().decode("utf-8"))
    assert "final_score" in result
    assert "breakdown" in result

    server.shutdown()
    server.server_close()
