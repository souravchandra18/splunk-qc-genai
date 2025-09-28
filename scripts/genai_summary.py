import openai, json, os
from textwrap import dedent

# --- Load logs ---
with open("output/logs.json") as f:
    logs = json.load(f)

# --- Load quantum anomaly findings ---
quantum_results = {}
try:
    with open("output/quantum_results.json") as f:
        quantum_results = json.load(f)
except FileNotFoundError:
    quantum_results = {"note": "No quantum results available."}

# --- Chunk logs for GPT analysis ---
CHUNK_SIZE = 300
chunks = [logs[i:i+CHUNK_SIZE] for i in range(0, len(logs), CHUNK_SIZE)]

summaries = []
for idx, chunk in enumerate(chunks):
    # Convert logs into readable format
    text_chunk = "\n".join([
        f"[{line.get('time', 'NA')}] {line.get('level', '')}: {line.get('message', str(line))}"
        if isinstance(line, dict) else str(line)
        for line in chunk
    ])

    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a log analysis assistant. Focus on anomalies, errors, and unusual patterns."},
            {"role": "user", "content": f"Analyze these logs (part {idx+1}):\n{text_chunk}"}
        ],
        temperature=0.3
    )

    summaries.append(f"### Chunk {idx+1} Summary\n" + response.choices[0].message.content.strip())

# --- Merge GPT Summaries ---
summaries_text = "\n\n".join(summaries)

# --- Build Final Prompt including Quantum results ---
final_prompt = dedent(f"""
You are a senior SRE. Based on these log summaries and quantum anomaly findings,
create a final incident report.

The report should include:
- High-level summary
- Detected anomalies
- Root cause analysis
- Quantum anomaly findings
- Impacted services
- Recommendations for fixes

### Quantum Findings:
{json.dumps(quantum_results, indent=2)}

### Log Summaries:
{summaries_text}
""")

final_response = openai.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a senior SRE generating RCA reports."},
        {"role": "user", "content": final_prompt}
    ],
    temperature=0.3
)

report = final_response.choices[0].message.content.strip()

# --- Save Final Report ---
os.makedirs("output", exist_ok=True)
with open("output/report.md", "w") as f:
    f.write(report)

print("✅ Report generated with quantum findings at output/report.md")
