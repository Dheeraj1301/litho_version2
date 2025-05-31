import pennylane as qml
from pennylane import numpy as np

n_qubits = 4
dev = qml.device("default.qubit", wires=n_qubits)

@qml.qnode(dev)
def circuit(params):
    for i in range(n_qubits):
        qml.RX(params[i], wires=i)
    return qml.expval(qml.PauliZ(0))

def cost(params):
    return 1 - circuit(params)

def optimize_parameters():
    init_params = np.random.rand(n_qubits, requires_grad=True)
    opt = qml.GradientDescentOptimizer(0.1)
    steps = 100

    for i in range(steps):
        init_params = opt.step(cost, init_params)
    return init_params
