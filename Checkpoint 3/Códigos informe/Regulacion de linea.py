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
Vreg_simu, Vo_simu = leer_txt_ltspice("RegLin_simu.txt")

df = pd.read_csv("RegLin_medida.csv")

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


plt.figure()

plt.plot(Vreg_simu, Vo_simu[:, 0], color = 'black', label='Simulación', linestyle='--')
plt.plot(Vreg_medida, Vo_medida, color = 'blue', label='Medición')

plt.xlabel(f'$V_{{reg}} [V]$')
plt.xlim(np.min(Vreg_medida), np.max(Vreg_medida))
plt.axvline(x = 6, linestyle = '--', color='red', linewidth=1, label='Vreg = 6V', alpha = 0.5)
plt.text(6.5, plt.ylim()[1]*0, '6V', ha='center', fontsize=9, color='red')
plt.legend()

plt.ylabel(f'$V_{{o}} [V]$')

plt.title("Regulación de Línea")
plt.grid()
plt.show()
plt.savefig("Regulacion_de_Linea.png")
