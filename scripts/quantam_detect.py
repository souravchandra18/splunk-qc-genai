import json
import pandas as pd
from qiskit_aer import AerSimulator
from qiskit.circuit.random import random_circuit
from qiskit import transpile

# Load logs
logs = pd.read_json("output/logs.json")

# --- Example Quantum Processing ---
# Instead of QuantumInstance, we just run directly on AerSimulator

# Create a toy quantum circuit
qc = random_circuit(4, 3, max_operands=3)

# Use AerSimulator
sim = AerSimulator()

# Transpile and run
compiled = transpile(qc, sim)
result = sim.run(compiled).result()

# Fake anomaly score (toy example: based on ERROR logs count + quantum random outcome)
error_count = (logs["level"] == "ERROR").sum()
counts = result.get_counts()
anomaly_score = error_count + (len(counts) % 5)

output = {
    "error_count": int(error_count),
    "quantum_counts": counts,
    "anomaly_score": anomaly_score
}

with open("output/quantum_results.json", "w") as f:
    json.dump(output, f, indent=2)

print("Quantum analysis done → output/quantum_results.json")
