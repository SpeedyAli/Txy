import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve

# Page setup
st.set_page_config(page_title="T-x-y and x-y Diagrams - Mohd Ali Khan", layout="centered")
st.title("T-x-y and x-y Diagram Analysis for Heptane-Octane Mixture")

markdown_equations = r"""
**Submitted by**: Mohd Ali Khan  
**To:** Prof. Imran Mohammad  
**Department of Petrochemical**  
**UIT RGPV, Bhopal**

---
### Assignment Overview
This assignment demonstrates the calculation and plotting of **T-x-y** and **x-y diagrams** for an ideal binary mixture (heptane + octane) using:
- **Raoult’s Law**
- **Antoine Equation**

These diagrams are useful in understanding phase behavior in distillation.

---
### 1. Antoine Equation
Used to calculate the **saturation pressure (Psat)** of each component:

$$
\log_{10}(P_{sat}) = A - \frac{B}{C + T}
$$

Where:
- \( T \) is temperature in °C  
- \( P_{sat} \) is in mmHg  

Antoine constants used:  
- **Heptane**: A = 6.893, B = 1260, C = 216  
- **Octane**: A = 6.9094, B = 1351, C = 217  

---
### 2. T-x-y Diagram (Temperature vs Mole Fractions)
**How it is calculated:**

1. For each liquid mole fraction \( x_H \) of heptane, calculate the bubble point temperature \( T \) by solving:  
   $$
   P_{total} = x_H \cdot P_H^{sat}(T) + x_O \cdot P_O^{sat}(T)
   $$

2. Then calculate vapor mole fraction \( y_H \):  
   $$
   y_H = \frac{x_H \cdot P_H^{sat}(T)}{P_{total}}
   $$
   $$
   y_O = 1 - y_H
   $$  
   $$
   P_{total} = 760\ \text{mmHg}
   $$

3. Plot \( T \) vs \( x \) and \( T \) vs \( y \).

---
### 3. x-y Diagram (Vapor vs Liquid Mole Fraction)
**How it is calculated:**

Once we calculate mole fraction \( x \) in liquid and corresponding \( y \) in vapor (from the T-x-y data), we simply:
- Plot \( x \) on X-axis  
- Plot \( y \) on Y-axis  
- Include diagonal reference line \( y = x \) for comparison  

This helps understand the separation behavior in distillation.

---
"""

# Antoine constants
antoine_constants = {
    "heptane": {"A": 6.893, "B": 1260.0, "C": 216.0},
    "octane": {"A": 6.9094, "B": 1351.0, "C": 217.0}
}

def antoine_eq(T, A, B, C):
    return 10**(A - B / (C + T))

P_total = 760  # mmHg

def bubble_point_temp(x_heptane):
    def func(T):
        P_heptane = antoine_eq(T, **antoine_constants["heptane"])
        P_octane = antoine_eq(T, **antoine_constants["octane"])
        x_octane = 1 - x_heptane
        return x_heptane * P_heptane + x_octane * P_octane - P_total
    T_guess = 100
    return fsolve(func, T_guess)[0]

x_vals = np.linspace(0, 1, 21)
T_vals = []
y_vals = []
table_data = []

for x in x_vals:
    T = bubble_point_temp(x)
    P_heptane = antoine_eq(T, **antoine_constants["heptane"])
    y = (x * P_heptane) / P_total
    T_vals.append(T)
    y_vals.append(y)
    table_data.append((round(x, 3), round(y, 3), round(T, 2)))

# Plot T-x-y diagram
st.subheader("T-x-y Diagram")
fig1, ax1 = plt.subplots()
ax1.plot(x_vals, T_vals, label='Liquid (x vs T)', marker='o', color='blue')
ax1.plot(y_vals, T_vals, label='Vapor (y vs T)', marker='s', color='red')
ax1.set_xlabel('Mole Fraction of Heptane')
ax1.set_ylabel('Temperature (°C)')
ax1.set_title('T-x-y Diagram for Heptane-Octane at 1 atm')
ax1.legend()
ax1.grid(True)
st.pyplot(fig1)

# Show data table
st.markdown("### Tabulated Data")
st.dataframe(
    {"x (Liquid Heptane)": [row[0] for row in table_data],
     "y (Vapor Heptane)": [row[1] for row in table_data],
     "T (°C)": [row[2] for row in table_data]}
)

# x-y diagram
st.subheader("x-y Diagram")
fig2, ax2 = plt.subplots()
ax2.plot(x_vals, y_vals, marker='d', color='green', label='x-y Curve')
ax2.plot([0, 1], [0, 1], '--', color='gray', label='y = x')
ax2.set_xlabel('Liquid Mole Fraction of Heptane (x)')
ax2.set_ylabel('Vapor Mole Fraction of Heptane (y)')
ax2.set_title('x-y Diagram for Heptane-Octane at 1 atm')
ax2.legend()
ax2.grid(True)
st.pyplot(fig2)

st.markdown("""
### Summary
This app demonstrates the phase behavior of ideal mixtures using **heptane and octane** as an example.
It calculates and visualizes the temperature and composition relationships in liquid-vapor equilibrium at constant pressure.
Such tools are valuable for understanding distillation and separation processes.
""")
