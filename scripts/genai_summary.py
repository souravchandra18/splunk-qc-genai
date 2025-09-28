import json
import openai
import os

openai.api_key = os.environ["OPENAI_API_KEY"]

with open("output/logs.json") as f:
    logs = json.load(f)

with open("output/quantum_results.json") as f:
    quantum = json.load(f)

prompt = f"""
Analyze these logs: {logs[:50]}
Quantum findings: {quantum}
Summarize anomalies and root causes.
"""

# ✅ Legacy Completion API for openai==0.28.0
response = openai.Completion.create(
    engine="text-davinci-003",  # or "gpt-4o", if available
    prompt=prompt,
    max_tokens=300,
    temperature=0.2
)

summary_text = response["choices"][0]["text"]

with open("output/report.md", "w") as f:
    f.write(summary_text)

print("GenAI summary done → output/report.md")
