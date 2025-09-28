import json
import pandas as pd
from qiskit_aer import AerSimulator
from qiskit import QuantumCircuit, transpile

# Load logs
logs = pd.read_json("output/logs.json")

# --- Quantum Processing ---
qc = QuantumCircuit(4, 4)
qc.h([0, 1, 2, 3])
qc.cx(0, 1)
qc.cx(2, 3)
qc.measure([0, 1, 2, 3], [0, 1, 2, 3])

sim = AerSimulator()
compiled = transpile(qc, sim)
result = sim.run(compiled, shots=100).result()

counts = result.get_counts()

# Calculate fake anomaly score
error_count = (logs["level"] == "ERROR").sum()
anomaly_score = error_count + (len(counts) % 5)

# ✅ Convert all values to JSON-safe types
output = {
    "error_count": int(error_count),
    "quantum_counts": {str(k): int(v) for k, v in counts.items()},
    "anomaly_score": int(anomaly_score)
}

with open("output/quantum_results.json", "w") as f:
    json.dump(output, f, indent=2)

print("Quantum analysis done → output/quantum_results.json")
