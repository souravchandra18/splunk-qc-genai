import json
import pandas as pd
from qiskit_aer import AerSimulator
from qiskit.circuit.random import random_circuit
from qiskit import transpile

# Load logs
logs = pd.read_json("output/logs.json")

# --- Quantum Processing ---
qc = random_circuit(4, 3, max_operands=3)

sim = AerSimulator()
compiled = transpile(qc, sim)
result = sim.run(compiled, shots=100).result()

# ✅ Fix: extract counts from the result dict directly
data_dict = result.data()
counts = list(data_dict.values())[0]["counts"]

# Fake anomaly score: ERROR logs + quantum counts
error_count = (logs["level"] == "ERROR").sum()
anomaly_score = error_count + (len(counts) % 5)

output = {
    "error_count": int(error_count),
    "quantum_counts": counts,
    "anomaly_score": anomaly_score
}

with open("output/quantum_results.json", "w") as f:
    json.dump(output, f, indent=2)

print("Quantum analysis done → output/quantum_results.json")
