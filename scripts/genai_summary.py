import openai, json, os

LOG_FILE = "output/logs.json"
QC_FILE = "output/quantum_results.json"
OUTPUT_FILE = "output/report.md"

with open(LOG_FILE) as f:
    logs = json.load(f)

with open(QC_FILE) as f:
    quantum = json.load(f)

openai.api_key = os.environ.get("OPENAI_API_KEY")

prompt = f"""
Analyze these logs (first 5000 entries for brevity):
{logs[:5000]}
Quantum findings:
{quantum}
Summarize anomalies, provide root cause analysis, and suggest recommended fixes.
"""

summary = openai.Completion.create(
    model="gpt-4o-mini",
    prompt=prompt,
    max_tokens=500
)

os.makedirs("output", exist_ok=True)
with open(OUTPUT_FILE,"w") as f:
    f.write(summary["choices"][0]["text"])

print(f"RCA summary saved to {OUTPUT_FILE}")
