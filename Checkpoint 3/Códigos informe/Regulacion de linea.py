import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# -------- FUNCION GENERAL PARA LEER ARCHIVOS DE LTSPICE --------
def leer_txt_ltspice(nombre_archivo):
    data = np.loadtxt(nombre_archivo, skiprows=1)
    x = data[:, 0]
    y = data[:, 1:]
    return x, y


# ============================================================
# 1) REGULACIÓN DE LÍNEA: Vo vs Vreg
# ============================================================
Vreg_simu, Vo_simu = leer_txt_ltspice("/Users/lautarogarciavitale/Desktop/UBA/Materias/CIRCUITOS 2/taller-de-circuitos-grupo-5/Checkpoint 3/Códigos informe/RegLin_simu.txt")

df = pd.read_csv("/Users/lautarogarciavitale/Desktop/UBA/Materias/CIRCUITOS 2/taller-de-circuitos-grupo-5/Checkpoint 3/Códigos informe/RegLin_medida.csv")

# reemplaza coma decimal por punto
df["Vreg"] = df["Vreg"].astype(str).str.replace(",", ".")
df["Vo"]   = df["Vo"].astype(str).str.replace(",", ".")

# convierte a float
df["Vreg"] = pd.to_numeric(df["Vreg"], errors='coerce')
df["Vo"]   = pd.to_numeric(df["Vo"], errors='coerce')

# elimina filas inválidas
df = df.dropna(subset=["Vreg", "Vo"])

Vreg_medida = df["Vreg"].to_numpy()
Vo_medida   = df["Vo"].to_numpy()

# ============================================================
# AJUSTE LINEAL EN LA ZONA REGULADA
# ============================================================

mask = Vreg_medida >= 6

x_fit = Vreg_medida[mask]
y_fit = Vo_medida[mask]

# ajuste lineal y = m*x + b
m, b = np.polyfit(x_fit, y_fit, 1)

# recta ajustada
y_ajuste = m*x_fit + b

plt.figure()

plt.plot(Vreg_simu, Vo_simu[:, 0], color = 'grey', label='Simulación', linestyle='--')
plt.plot(Vreg_medida, Vo_medida, color = 'black', label='Medición', linewidth=2.5, marker='o', markersize=5)
plt.plot(x_fit, y_ajuste, color='cyan', linewidth=1.5, linestyle='-.', label=f'RegLin =  {m*1000:.2f} mV/V'.replace('.', ','))

plt.xlabel(r'$V_\mathrm{{REG}} \quad [\mathrm{V}]$')
plt.xlim(np.min(Vreg_medida), np.max(Vreg_medida))
plt.axvline(x = 6, linestyle = '--', color='red', linewidth=1.5, label=r'$V_\mathrm{{REG}}^\mathrm{{min}}|_{{V_{{O}} = 5\,\mathrm{{V}}}}$', alpha = 0.5)
plt.text(6.5, 0.5, '6 V', ha='center', fontsize=9, color='red')
plt.legend()

plt.ylabel(r'$V_{{O}} \quad [\mathrm{V}]$')

plt.title("Regulación de Línea")
plt.grid()
plt.savefig("/Users/lautarogarciavitale/Desktop/UBA/Materias/CIRCUITOS 2/taller-de-circuitos-grupo-5/Checkpoint 3/Códigos informe/reg_lin.png", dpi=300, bbox_inches='tight')
plt.show()