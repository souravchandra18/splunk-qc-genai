import os, requests, json
from datetime import datetime, timedelta
from faker import Faker
import random, uuid

OUTPUT_FILE = "output/logs.json"

def fetch_fake_logs(n=5000, anomaly_rate=0.01):
    fake = Faker()
    logs = []
    services = ["auth","payments","orders","inventory","gateway"]
    levels = ["DEBUG","INFO","WARN","ERROR"]
    start_ts = datetime.utcnow() - timedelta(hours=1)
    
    for i in range(n):
        ts = start_ts + timedelta(seconds=i)
        rec = {
            "timestamp": ts.isoformat() + "Z",
            "service": random.choice(services),
            "level": random.choices(levels, weights=[60,200,30,10])[0],
            "host": f"{random.choice(services)}-host-{random.randint(1,20)}",
            "message": fake.sentence(),
            "request_id": str(uuid.uuid4()),
            "trace_id": str(uuid.uuid4()),
            "latency_ms": max(1, int(random.gauss(120,80))),
            "env": random.choice(["prod","staging","dev"]),
            "region": random.choice(["us-east-1","eu-west-1"])
        }
        if random.random() < anomaly_rate:
            rec["level"]="ERROR"
            rec["message"]="[ANOMALY] " + rec["message"]
            rec["latency_ms"] *= random.randint(5,20)
            rec["error_code"]=random.choice(["DB_CONN_TIMEOUT","401","429","OOM"])
        logs.append(rec)
    return logs

def fetch_splunk_logs():
    splunk_url = os.environ.get("SPLUNK_URL")
    user = os.environ.get("SPLUNK_USER")
    pwd = os.environ.get("SPLUNK_PASS")
    query = "search index=prod_logs error OR timeout earliest=-1h latest=now()"
    
    resp = requests.get(f"{splunk_url}/services/search/jobs/export",
                        auth=(user,pwd),
                        params={"search": query, "output_mode":"json"})
    logs = [json.loads(line) for line in resp.text.splitlines() if line]
    return logs

if __name__=="__main__":
    os.makedirs("output", exist_ok=True)
    use_fake = os.environ.get("USE_FAKE_LOGS","1") == "1"
    if use_fake:
        logs = fetch_fake_logs(n=5000)
    else:
        logs = fetch_splunk_logs()
    with open(OUTPUT_FILE,"w") as f:
        json.dump(logs,f)
    print(f"Fetched {len(logs)} logs to {OUTPUT_FILE}")
