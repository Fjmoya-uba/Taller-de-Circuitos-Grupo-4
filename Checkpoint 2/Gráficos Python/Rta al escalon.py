import numpy as np
import matplotlib.pyplot as plt

# --- CONFIGURACIÓN ---
archivo1 = "archivos de texto/LC escalon (sin compensar).txt"
archivo2 = "archivos de texto/LC escalon (compensado).txt"

# --- FUNCIÓN PARA CARGAR DATOS ---
def cargar_datos(nombre_archivo):
    # Intenta cargar ignorando líneas no numéricas (headers típicos de LTspice)
    data = []
    with open(nombre_archivo, 'r') as f:
        for linea in f:
            try:
                valores = [float(x) for x in linea.strip().split()]
                data.append(valores)
            except:
                continue  # ignora headers o líneas inválidas

    data = np.array(data)
    t = data[:, 0]
    y = data[:, 1]
    return t, y

# --- CARGA DE DATOS ---
t1, y1 = cargar_datos(archivo1)
t2, y2 = cargar_datos(archivo2)

# --- GRÁFICO 1 ---
plt.figure()
plt.plot(t1, y1, 'k')  # 'k' = negro
plt.xlabel("t [s]")
plt.ylabel(f'$V_o$ [V]')
plt.title(f'$C_L = 15 \mu F$, $R_L = 1 \Omega$')
plt.xlim(t1.min(), t1.max())
plt.grid(True)

plt.savefig("Rta al escalon LC (sin compensar).png", dpi=300)
# --- GRÁFICO 2 ---
plt.figure()
plt.plot(t2, y2, 'k')
plt.xlabel("t [s]")
plt.ylabel(f'$V_o$ [V]')
plt.title(f'$C_L = 15 \mu F$, $R_L = 1 \Omega$')
plt.xlim(t2.min(), t2.max())
plt.grid(True)

plt.savefig("Rta al escalon LC(compensada).png", dpi=300)
plt.show()