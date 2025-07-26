
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# === Title ===
st.title("Solow–Swan Model with Technological Progress")

# === Parameters ===
T = 300
s = st.slider("Savings rate (s)", 0.01, 0.99, 0.18, step=0.01)
delta = st.slider("Depreciation rate (δ)", 0.01, 0.99, 0.03, step=0.01)
n = st.slider("Population growth rate (n)", 0.0, 0.2, 0.01, step=0.01)
g = st.slider("Technological progress rate (g)", 0.0, 0.2, 0.01, step=0.01)
alpha = st.slider("Capital share in output (α)", 0.01, 0.99, 1/3, step=0.01)

k0 = 10.0
A0 = 10.0
L0 = 30.0

# === Simulation Function ===
def simulate_solow_tech(T, s, delta, n, g, alpha, k0, A0, L0):
    k = [k0]
    A = [A0]
    L = [L0]
    y = []
    sy = []
    c = []
    K = []
    Y = []
    sY = []
    C = []
    k_pc = []
    y_pc = []
    sy_pc = []
    c_pc = []

    for t in range(T):
        kt = k[t]
        At = A[t]
        Lt = L[t]
        yt = kt ** alpha
        syt = s * yt
        ct = (1 - s) * yt
        Kt = kt * At * Lt
        Yt = yt * At * Lt
        sYt = syt * At * Lt
        Ct = ct * At * Lt
        kpc = kt * At
        ypc = yt * At
        sypc = syt * At
        cpc = ct * At

        y.append(yt)
        sy.append(syt)
        c.append(ct)
        K.append(Kt)
        Y.append(Yt)
        sY.append(sYt)
        C.append(Ct)
        k_pc.append(kpc)
        y_pc.append(ypc)
        sy_pc.append(sypc)
        c_pc.append(cpc)

        if t < T - 1:
            k_next = kt + (s * yt - (n + g + delta) * kt)
            A_next = At * (1 + g)
            L_next = Lt * (1 + n)
            k.append(k_next)
            A.append(A_next)
            L.append(L_next)

    return np.arange(T), k, y, sy, c, k_pc, y_pc, sy_pc, c_pc, K, Y, sY, C

# === Steady state values ===
k_hat_star = (s / (n + g + delta)) ** (1 / (1 - alpha))
y_hat_star = k_hat_star ** alpha
sy_hat_star = s * y_hat_star
c_hat_star = (1 - s) * y_hat_star

st.markdown("### Steady State Values (per unit of effective labor)")
st.latex(r"\hat{k}^* = " + f"{k_hat_star:.4f}")
st.latex(r"\hat{y}^* = " + f"{y_hat_star:.4f}")
st.latex(r"s \hat{y}^* = " + f"{sy_hat_star:.4f}")
st.latex(r"\hat{c}^* = " + f"{c_hat_star:.4f}")

# === Run simulation ===
t, k, y, sy, c, k_pc, y_pc, sy_pc, c_pc, K, Y, sY, C = simulate_solow_tech(T, s, delta, n, g, alpha, k0, A0, L0)

# === Select view type ===
view = st.selectbox("Select variable view", ["Per unit of effective labor", "Per capita", "Aggregate"])

if view == "Per unit of effective labor":
    labels_eff = ['k̂(t)', 'ŷ(t)', 's·ŷ(t)', 'ĉ(t)']
    data_eff = [k, y, sy, c]
    for label, series in zip(labels_eff, data_eff):
        fig, ax = plt.subplots()
        ax.plot(t, series)
        ax.set_title(f"{label}")
        ax.set_xlabel("Period")
        ax.set_ylabel(label)
        ax.grid(True)
        st.pyplot(fig)

elif view == "Per capita":
    fig, ax = plt.subplots()
    for var, label in zip([k_pc, y_pc, sy_pc, c_pc], ['k p.c.', 'y p.c.', 'sy p.c.', 'c p.c.']):
        ax.plot(t, var, label=label)
    ax.set_title("Per Capita Variables Over Time")
    ax.set_xlabel("Period")
    ax.grid(True)
    ax.legend()
    st.pyplot(fig)

elif view == "Aggregate":
    fig, ax = plt.subplots()
    for var, label in zip([K, Y, sY, C], ['K(t)', 'Y(t)', 'sY(t)', 'C(t)']):
        ax.plot(t, var, label=label)
    ax.set_title("Aggregate Variables Over Time")
    ax.set_xlabel("Period")
    ax.grid(True)
    ax.legend()
    st.pyplot(fig)
