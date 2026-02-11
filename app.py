import streamlit as st
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_bloch_vector
import matplotlib.pyplot as plt

# ----------------------------------------
# Page setup
# ----------------------------------------
st.set_page_config(page_title="BCH Codes with Quantum Demo", layout="wide")
st.title("🔐 Binary BCH Codes & Berlekamp Algorithm (Quantum Demonstration)")

# ----------------------------------------
# Helper Functions
# ----------------------------------------

def xor_division(dividend, divisor):
    """Modulo-2 division"""
    dividend = dividend.copy()
    for i in range(len(dividend) - len(divisor) + 1):
        if dividend[i] == 1:
            for j in range(len(divisor)):
                dividend[i + j] ^= divisor[j]
    return dividend[-(len(divisor) - 1):]

def compute_syndrome(received, generator):
    return xor_division(received, generator)

def simple_berlekamp_like_decoder(received, syndrome):
    """
    Simplified educational decoder:
    Tries single-bit error correction
    """
    if all(s == 0 for s in syndrome):
        return received, "No error detected"

    for i in range(len(received)):
        test = received.copy()
        test[i] ^= 1
        if all(s == 0 for s in compute_syndrome(test, generator)):
            return test, f"Single-bit error corrected at position {i}"

    return received, "Unable to correct (multiple errors)"

def quantum_visualization(bits):
    qc = QuantumCircuit(len(bits))
    for i, b in enumerate(bits):
        if b == 1:
            qc.x(i)
    state = Statevector.from_instruction(qc)
    return qc, state

# ----------------------------------------
# Sidebar Inputs
# ----------------------------------------
st.sidebar.header("BCH Parameters (Example)")
st.sidebar.markdown("Example: (7,4) BCH-like code")

generator = st.sidebar.text_input(
    "Generator Polynomial (binary)",
    "1011"
)
generator = [int(x) for x in generator]

received_str = st.sidebar.text_input(
    "Received Codeword (binary)",
    "1101001"
)
received = [int(x) for x in received_str]

# ----------------------------------------
# Syndrome Calculation
# ----------------------------------------
st.header("📌 Syndrome Calculation")

syndrome = compute_syndrome(received, generator)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Received Vector")
    st.write(received)

with col2:
    st.subheader("Syndrome")
    st.write(syndrome)

# ----------------------------------------
# Berlekamp Decoding
# ----------------------------------------
st.header("🧮 Berlekamp-Style Decoding (Educational)")

corrected, message = simple_berlekamp_like_decoder(received, syndrome)

st.success(message)
st.write("Corrected Codeword:", corrected)

# ----------------------------------------
# Quantum Demonstration
# ----------------------------------------
st.header("⚛️ Quantum Representation of Received Codeword")

qc, state = quantum_visualization(received)

col3, col4 = st.columns(2)

with col3:
    st.subheader("Quantum Circuit")
    st.pyplot(qc.draw(output="mpl"))

with col4:
    st.subheader("Bloch Sphere (Single Qubit Demonstration)")

    # Bloch sphere shown for first qubit only
    if received[0] == 0:
        bloch_vec = [0, 0, 1]   # |0⟩
    else:
        bloch_vec = [0, 0, -1]  # |1⟩

    fig = plot_bloch_vector(bloch_vec)
    st.pyplot(fig)

# ----------------------------------------
# Explanation
# ----------------------------------------
st.info("""
**Note:**
- BCH encoding and Berlekamp decoding are classical.
- Quantum circuit demonstrates how classical bits are mapped to qubits.
- Bloch sphere is shown for a single qubit since multi-qubit states
  cannot be represented on a single Bloch sphere.
""")
