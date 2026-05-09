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

Vreg_simu, Vo_simu = leer_txt_ltspice("/Users/lautarogarciavitale/Desktop/UBA/Materias/CIRCUITOS 2/taller-de-circuitos-grupo-5/Checkpoint 3/Códigos informe/Regulación de Línea/RegLin_simu.txt")

df = pd.read_csv("/Users/lautarogarciavitale/Desktop/UBA/Materias/CIRCUITOS 2/taller-de-circuitos-grupo-5/Checkpoint 3/Códigos informe/Regulación de Línea/RegLin_medida.csv")

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


# AJUSTE LINEAL EN LA ZONA REGULADA

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
plt.plot(x_fit, y_ajuste, color='cyan', linewidth=1.5, linestyle='-.', label = rf'$\mathrm{{Reg}}_{{\mathrm{{lín}}}} = {m*1000:.2f}\,\mathrm{{mV/V}}$'.replace('.', ','))

plt.xlabel(r'$V_\mathrm{{REG}} \quad [\mathrm{V}]$')
plt.xlim(np.min(Vreg_medida), np.max(Vreg_medida))
plt.axvline(x = 6, linestyle = '--', color='red', linewidth=1.5, label=r'$V_\mathrm{{REG}}^\mathrm{{min}}|_{{V_{{o}} = 5\,\mathrm{{V}}}}$', alpha = 0.5)
plt.text(6.5, 0.5, '6 V', ha='center', fontsize=9, color='red')
plt.legend()

plt.ylabel(r'$V_{{o}} \quad [\mathrm{V}]$')

plt.title("Regulación de Línea")
plt.grid()
plt.savefig("/Users/lautarogarciavitale/Desktop/UBA/Materias/CIRCUITOS 2/taller-de-circuitos-grupo-5/Checkpoint 3/Códigos informe/Regulación de Línea/reg_lin.png", dpi=300, bbox_inches='tight')
#plt.show()

# ============================================================
# 2) EFICIENCIA: eta vs Vreg
# ============================================================

Vreg_medida, eta_medida = leer_txt_ltspice("/Users/lautarogarciavitale/Desktop/UBA/Materias/CIRCUITOS 2/taller-de-circuitos-grupo-5/Checkpoint 3/Códigos informe/Eficiencia/Vreg.txt")

# como la función devuelve y como matriz columna:
eta_medida = eta_medida[:, 0]

plt.figure()
plt.plot(Vreg_medida, eta_medida, color='black', linewidth=2.5, marker='o', markersize=5)
plt.xlabel(r'$V_\mathrm{REG} \quad [\mathrm{V}]$')
plt.ylabel(r'$\eta \quad [\%]$')
plt.title(f"Eficiencia vs. Tensión de entrada @ $I_o = 1$ A")
plt.xlim(np.min(Vreg_medida), np.max(Vreg_medida))
plt.grid()
plt.savefig("/Users/lautarogarciavitale/Desktop/UBA/Materias/CIRCUITOS 2/taller-de-circuitos-grupo-5/Checkpoint 3/Códigos informe/Eficiencia/eficiencia_vs_vreg.png", dpi=300, bbox_inches='tight')
#plt.show()

# ============================================================
# 2) EFICIENCIA: eta vs Io
# ============================================================

Io_medida, eta_medida = leer_txt_ltspice("/Users/lautarogarciavitale/Desktop/UBA/Materias/CIRCUITOS 2/taller-de-circuitos-grupo-5/Checkpoint 3/Códigos informe/Eficiencia/Io.txt")

# como la función devuelve y como matriz columna:
eta_medida = eta_medida[:, 0]

plt.figure()
plt.plot(Io_medida, eta_medida, color='black', linewidth=2.5, marker='o', markersize=5)
plt.xlabel(r'$I_o \quad [\mathrm{A}]$')
plt.ylabel(r'$\eta \quad [\%]$')
plt.title(r"Eficiencia vs. Corriente de salida @ $V_\mathrm{REG} = 9,5$ V")
plt.grid()
plt.savefig("/Users/lautarogarciavitale/Desktop/UBA/Materias/CIRCUITOS 2/taller-de-circuitos-grupo-5/Checkpoint 3/Códigos informe/Eficiencia/eficiencia_vs_io.png", dpi=300, bbox_inches='tight')
#plt.show()

# ============================================================
# 3) REGULACIÓN DE CARGA: Vo vs Req
# ============================================================

Req_simu, Vo_simu = leer_txt_ltspice("/Users/lautarogarciavitale/Desktop/UBA/Materias/CIRCUITOS 2/taller-de-circuitos-grupo-5/Checkpoint 3/Códigos informe/Regulación de Carga/RegCar_simu.txt")

Req_medida, Vo_medida = leer_txt_ltspice("/Users/lautarogarciavitale/Desktop/UBA/Materias/CIRCUITOS 2/taller-de-circuitos-grupo-5/Checkpoint 3/Códigos informe/Regulación de Carga/RegCar_med.txt")

# como la función devuelve matrices columna:
Vo_simu   = Vo_simu[:, 0]
Vo_medida = Vo_medida[:, 0]

indices = np.argsort(Req_medida)
Req_medida = Req_medida[indices]
Vo_medida  = Vo_medida[indices]

plt.figure()
plt.plot(Req_simu, Vo_simu, color='grey', linestyle='--', label='Simulación')
plt.plot(Req_medida, Vo_medida, color='black', linewidth=2.5, marker='o', markersize=5, label='Medición')
plt.xlabel(r'$R_L \quad [\Omega]$')
plt.ylabel(r'$V_o \quad [\mathrm{V}]$')
plt.title("Regulación de Carga")
plt.xlim(np.min(Req_medida), np.max(Req_medida))
plt.grid()
plt.legend()
plt.savefig("/Users/lautarogarciavitale/Desktop/UBA/Materias/CIRCUITOS 2/taller-de-circuitos-grupo-5/Checkpoint 3/Códigos informe/Regulación de Carga/reg_car.png", dpi=300, bbox_inches='tight')
#plt.show()

# ============================================================
# 4) FOLDBACK: Vo vs Io
# ============================================================

data_simu = np.loadtxt("/Users/lautarogarciavitale/Desktop/UBA/Materias/CIRCUITOS 2/taller-de-circuitos-grupo-5/Checkpoint 3/Códigos informe/Foldback/foldback_simu.txt", skiprows=1, dtype=str)

# convierte a float
data_simu = data_simu.astype(float)

# columnas:
# 0 -> RL (se desprecia)
# 1 -> Io
# 2 -> Vo
Io_simu = data_simu[:, 2]
Vo_simu = data_simu[:, 1]

Io_medida, Vo_medida = leer_txt_ltspice("/Users/lautarogarciavitale/Desktop/UBA/Materias/CIRCUITOS 2/taller-de-circuitos-grupo-5/Checkpoint 3/Códigos informe/Foldback/foldback_med.txt")

Vo_medida = Vo_medida[:, 0]

# AJUSTE LINEAL EN LA ZONA REGULADA

mask = (Vo_medida > 4.5) & (Io_medida < 1.5)

x_fit = Io_medida[mask]
y_fit = Vo_medida[mask]

# ajuste lineal: Vo = m*Io + b
m, b = np.polyfit(x_fit, y_fit, 1)

# recta ajustada
y_ajuste = m*x_fit + b

plt.figure()
plt.plot(Io_simu, Vo_simu, color='grey', linestyle='--', label='Simulación')
plt.plot(Io_medida, Vo_medida, color='black', linewidth=2.5, marker='o', markersize=5, label='Medición')
plt.plot(x_fit, y_ajuste, color='cyan', linewidth=1.5, linestyle='-.', label = rf'$\mathrm{{Reg}}_{{\mathrm{{car}}}} = {m*(-1000):.2f}\,\mathrm{{m\Omega}}$'.replace('.', ','))
plt.xlabel(r'$I_o \quad [\mathrm{A}]$')
plt.ylabel(r'$V_o \quad [\mathrm{V}]$')
plt.title(r"Característica $\mathit{foldback}$")
plt.grid()
plt.legend()
plt.savefig("/Users/lautarogarciavitale/Desktop/UBA/Materias/CIRCUITOS 2/taller-de-circuitos-grupo-5/Checkpoint 3/Códigos informe/Foldback/foldback.png", dpi=300, bbox_inches='tight')
plt.show()