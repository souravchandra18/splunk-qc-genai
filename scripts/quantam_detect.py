import pandas as pd, json
from qiskit_aer import AerSimulator
from qiskit_utils import QuantumInstance
from qiskit.algorithms import QAOA
from qiskit_optimization import QuadraticProgram

LOG_FILE = "output/logs.json"
OUTPUT_FILE = "output/quantum_results.json"

# Load logs
logs = pd.read_json(LOG_FILE)

# QAOA: minimize number of error clusters
qp = QuadraticProgram()
for i in range(len(logs)):
    qp.binary_var(name=f"x{i}")

qp.minimize(linear=[1]*len(logs))

backend = AerSimulator()
qaoa = QAOA(quantum_instance=QuantumInstance(backend))
result = qaoa.compute_minimum_eigenvalue(qp.to_ising()[0])

with open(OUTPUT_FILE,"w") as f:
    json.dump({"result": str(result)},f)

print(f"Quantum results saved to {OUTPUT_FILE}")
