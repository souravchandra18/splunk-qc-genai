import os
import json
import openai

# Set API key
openai.api_key = os.environ["OPENAI_API_KEY"]

# Load logs and quantum results
with open("output/logs.json") as f:
    logs = json.load(f)

with open("output/quantum_results.json") as f:
    quantum = json.load(f)

# Prepare the prompt
prompt_text = f"""
Analyze these logs: {logs[:500]}
Quantum findings: {quantum}
Summarize anomalies and root causes.
"""

# âœ… New ChatCompletion API
response = openai.chat.completions.create(
    model="gpt-4o-mini",  # or gpt-4, gpt-3.5-turbo
    messages=[{"role": "user", "content": prompt_text}],
    temperature=0.2,
    max_tokens=300
)

# Extract text
summary_text = response.choices[0].message.content

# Save report
with open("output/report.md", "w") as f:
    f.write(summary_text)

print("GenAI summary done â†’ output/report.md")
