import json
import pandas as pd
from qiskit_aer import AerSimulator
from qiskit import QuantumCircuit, transpile

# Load logs
logs = pd.read_json("output/logs.json")

# --- Quantum Processing ---

# Create a simple 4-qubit circuit
qc = QuantumCircuit(4, 4)

# Add some random operations (toy example)
qc.h([0, 1, 2, 3])
qc.cx(0, 1)
qc.cx(2, 3)

# Measure all qubits
qc.measure([0,1,2,3], [0,1,2,3])

# Use AerSimulator
sim = AerSimulator()

# Transpile and run
compiled = transpile(qc, sim)
result = sim.run(compiled, shots=100).result()

# ✅ Get counts reliably
counts = result.get_counts()

# Fake anomaly score: ERROR logs + quantum counts length
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
