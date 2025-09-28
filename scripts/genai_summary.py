import os
import json
import openai

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

response = openai.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.2,
    max_tokens=300
)

summary_text = response.choices[0].message.content

with open("output/report.md", "w") as f:
    f.write(summary_text)

print("GenAI summary done → output/report.md")
