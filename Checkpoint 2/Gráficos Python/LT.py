import numpy as np
import matplotlib.pyplot as plt
import re

# ====== PARSER ======
def parse_bode_file(filename):
    with open(filename, 'r', encoding='cp1252') as f:
        lines = f.readlines()

    data = {}
    current_label = None

    for line in lines:
        line = line.strip()

        if "Step Information" in line:
            current_label = line
            data[current_label] = {"freq": [], "mag": [], "phase": []}
            continue

        if line.startswith("Freq") or line == "":
            continue

        try:
            parts = line.split('\t')
            freq = float(parts[0])

            match = re.search(r'\(([^d]+)dB,([^\)]+)°\)', parts[1])
            mag = float(match.group(1))
            phase = float(match.group(2))

            data[current_label]["freq"].append(freq)
            data[current_label]["mag"].append(mag)
            data[current_label]["phase"].append(phase)

        except:
            continue

    return data


# ====== CRUCE POR 0 dB ======
def find_gain_crossing(freq, mag, phase):
    freq = np.array(freq)
    mag = np.array(mag)
    phase = np.array(phase)

    idx = np.where(np.diff(np.sign(mag)))[0]

    if len(idx) == 0:
        return None, None

    i = idx[0]

    # Interpolación
    f1, f2 = freq[i], freq[i+1]
    m1, m2 = mag[i], mag[i+1]
    p1, p2 = phase[i], phase[i+1]

    f_gc = f1 + (0 - m1) * (f2 - f1) / (m2 - m1)
    phase_gc = p1 + (f_gc - f1) * (p2 - p1) / (f2 - f1)

    return f_gc, phase_gc


# ====== MAIN ======
data = parse_bode_file("archivos de texto/LC compensado.txt")

# ====== UN GRÁFICO POR CADA CL ======

label1 = "Step Information: $C_L$ = 1µF, $R_L$ = 1 Ω"
label2 = "Step Information: $C_L$ = 15µF, $R_L$ = 1 Ω"

for label, d in data.items():
    freq = np.array(d["freq"])
    mag = np.array(d["mag"])
    phase = np.array(d["phase"])
    phase_rad = np.deg2rad(phase)

    #Unwrap
    phase_unwrapped = np.unwrap(phase_rad)
    phase = np.rad2deg(phase_unwrapped)

    f_gc, phase_gc = find_gain_crossing(freq, mag, phase)

    plt.figure(figsize=(8, 6))

    # --- MAGNITUD ---
    plt.subplot(2, 1, 1)
    plt.semilogx(freq, mag, color = 'black')

    plt.axhline(0, color = 'black',linestyle='--')

    if f_gc is not None:
        plt.plot(f_gc, 0, 'o')

    plt.ylabel("Magnitud [dB]")
    if '1µ' in label:
        plt.title(f'Bode para $C_L$ = 1µF, $R_L$ = 1 Ω')
    else:
        plt.title(f'Bode para $C_L$ = 15µF, $R_L$ = 1 Ω')
    plt.grid(True, which="both")
    plt.xlim(freq.min(), freq.max())

    # --- FASE ---
    plt.subplot(2, 1, 2)
    plt.semilogx(freq, phase, color = 'black')

    if f_gc is not None:
        plt.plot(f_gc, phase_gc, 'o')
        plt.text(f_gc, phase_gc + 15, f"{phase_gc:.1f}°")

    plt.xlabel("Frecuencia [Hz]")
    plt.ylabel("Fase [°]")
    plt.grid(True, which="both")
    plt.xlim(freq.min(), freq.max())

    if '1µ' in label:
        plt.savefig("LC compensado 1uF.png", dpi=300)
    else:
        plt.savefig("LC compensado 15uF.png", dpi=300)

plt.tight_layout()


plt.show()