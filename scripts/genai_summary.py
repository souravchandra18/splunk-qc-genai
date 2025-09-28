import openai, json, time, os
from textwrap import dedent
from openai.error import RateLimitError

# ---------------------------
# Helper: Safe GPT call with retries
# ---------------------------
def safe_chat_completion(**kwargs):
    for attempt in range(5):  # retry up to 5 times
        try:
            return openai.chat.completions.create(**kwargs)
        except RateLimitError:
            wait = (2 ** attempt) * 5  # exponential backoff
            print(f"⚠️ Rate limit hit. Retrying in {wait}s...")
            time.sleep(wait)
    raise RuntimeError("Failed after retries due to rate limits")

# ---------------------------
# Load Logs
# ---------------------------
with open("output/logs.json") as f:
    logs = json.load(f)

# Chunk logs
CHUNK_SIZE = 1000  # bigger chunks to reduce GPT calls
chunks = [logs[i:i+CHUNK_SIZE] for i in range(0, len(logs), CHUNK_SIZE)]

summaries = []
for idx, chunk in enumerate(chunks):
    text_chunk = "\n".join([str(line) for line in chunk])
    response = safe_chat_completion(
        model="gpt-4o-mini",   # or "gpt-3.5-turbo" if rate limits are too strict
        messages=[
            {"role": "system", "content": "You are a log analysis assistant."},
            {"role": "user", "content": f"Analyze these logs (part {idx+1}):\n{text_chunk}"}
        ],
        temperature=0.3
    )
    summaries.append(response.choices[0].message.content.strip())

# ---------------------------
# Load Quantum Results
# ---------------------------
quantum_results = {}
if os.path.exists("output/quantum_results.json"):
    with open("output/quantum_results.json") as f:
        quantum_results = json.load(f)

# ---------------------------
# Merge into Final Report
# ---------------------------
final_prompt = dedent(f"""
You are a senior SRE generating a detailed RCA report.

Here are summaries of logs:
{summaries}

Here are quantum anomaly findings:
{json.dumps(quantum_results, indent=2)}

Create a final report in markdown format with:
1. Detected anomalies
2. Root cause analysis
3. Quantum anomaly contributions
4. Recommendations
5. Overall summary
""")

final_response = safe_chat_completion(
    model="gpt-4o-mini",   # change to "gpt-3.5-turbo" if you hit rate limits often
    messages=[
        {"role": "system", "content": "You are a senior SRE generating RCA reports."},
        {"role": "user", "content": final_prompt}
    ],
    temperature=0.3
)

report = final_response.choices[0].message.content.strip()

# ---------------------------
# Save Final Report
# ---------------------------
with open("output/report.md", "w") as f:
    f.write(report)

print("✅ Final report generated → output/report.md")
