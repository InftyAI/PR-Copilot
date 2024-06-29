import requests

resp = requests.post(
    "http://localhost:8000/agent/pr-summary",
    json={"url": "https://github.com/InftyAI/PR-Copilot/pull/1"},
)
print(resp.json())
