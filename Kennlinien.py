import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
# 1: Glühlampe
U1 = [2.04, 3.88, 6.07, 8.01, 10.02, 12.00, 14.02, 15.93, 17.96, 19.87, 21.9, 23.8, 25.8, 27.8, 29.8, 31.7, 33.7, 35.9, 37.8, 39.8, 41.9, 43.9, 45.9, 47.9, 49.9, 51.9, 53.8, 55.8, 57.8, 59.8, 61.7, 63.7, 65.8, 67.9, 69.8, 71.7, 73.8, 75.9, 78, 80.1]
I1 = np.array([1.035, 2.17, 3.26, 4.33, 5.47, 6.60, 7.77, 8.89, 10.09, 11.23, 12.47, 13.67, 14.86, 16.10, 17.40, 18.64, 19.90, 21.4, 22.7, 24.0, 25.4, 26.8, 28.1, 29.5, 30.9, 32.3, 33.7, 35.1, 36.5, 37.9, 38.4, 40.8, 42.3, 43.4, 45.3, 46.8, 48.4, 50.0, 51.6, 53.2])*1e-4

'''plt.figure()
plt.plot(U1, I1, color='orange')
plt.title("Kennlinie Glühlampe")
plt.xlabel("Spannung U [V]")
plt.ylabel("Stromstärke I [A]")
plt.grid(True)
plt.show()'''

#part1 1/2
P = np.array(U1)*np.array(I1) # Leistung
R1 = np.array(U1)/np.array(I1) # widerstand
r = -(R1 - R1[0])/R1[0]  #relative widerstandsänderung
'''plt.figure()
plt.loglog(P,r)
plt.grid(True, which="both", ls='--')
plt.title("Kennlinien Glühlampe")
plt.xlabel("Lesitung P [W]")
plt.ylabel("relative Widerstandsänderung")
plt.show()'''
#part 1 2
# Konstanten:
T0 = 293.15        # Umgebungstemperatur [K]
sigma = 5.670374e-8  # Stefan-Boltzmann-Konstante

# Verwende nur Punkte, die nicht exakt null sind
mask = r != 0
P_fit = P[mask]
r_fit = r[mask]

# Modell: P = K * ( (T0 - r/c)^4 - T0^4 )
def model(r_var, K, c):
    dT = r_var / c     
    return K * ((T0 + dT)**4 - T0**4)

# Startwerte
K0 = np.mean(P_fit) / (((T0 + 100)**4) - T0**4)
c0 = 0.01
p0 = [K0, c0]
bounds = ([0, 0], [np.inf, np.inf])

# Fit
popt, pcov = curve_fit(model, r_fit, P_fit, p0=p0, bounds=bounds, maxfev=10000)
K_fit, c_fit = popt
perr = np.sqrt(np.diag(pcov))
A_fit = K_fit / sigma

print(f"Fit-Ergebnisse:")
print(f"K = {K_fit:.3e} ± {perr[0]:.3e}  (K = σ·A)")
print(f"c = {c_fit:.3e} ± {perr[1]:.3e}  (r = c·ΔT → ΔT = r/c)")
print(f"A = {A_fit:.3e} m²")

# Plot: Daten und Modell
r_plot = np.linspace(min(r_fit), max(r_fit), 200)
P_model = model(r_plot, K_fit, c_fit)

plt.figure(figsize=(6,4))
plt.plot(r_fit, P_fit, 'o', label='Messdaten')
plt.plot(r_plot, P_model, '-', label='Fit')
plt.xlabel("relative Widerstandsänderung r")
plt.ylabel("Leistung P [W]")
plt.title("Fit: Stefan-Boltzmann-Modell mit ΔT = r/c")
plt.legend()
plt.grid(True)
plt.show()
#Temp
T_fit = T0 + r_fit / c_fit
plt.plot(P_fit, T_fit)
plt.show()

T_from_P = (T0**4 + P_fit / (sigma * A_fit))**0.25

plt.plot(P_fit, T_fit, 'o', label='aus r/c')
plt.plot(P_fit, T_from_P, '-', label='aus Stefan-Boltzmann')
plt.xlabel("Leistung P [W]")
plt.ylabel("Temperatur T [K]")
plt.legend()
plt.grid(True)
plt.show()


# 2: Diode
U2 = [0, 0.51, 0.616, 0.642, 0.706, 0.744, 0.746]
I2 = [0, 0.01, 0.565, 1.535, 18.36, 82.0, 92]

'''plt.figure()
plt.plot(U2, I2, color='red')
plt.title("Kennlinie Diode")
plt.xlabel("Spannung U [V]")
plt.ylabel("Stromstärke I [mA]")
plt.grid(True)
plt.show()'''

# 3: Diode andersrum
U3e = [0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4, 5, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 10, 11, 12, 13, 14, 15, 16, 17]
I3 = [0, 0, 0, 0, 0, 0, 0, 0, 0.02, 0.40, 0.47, 4.23, 8.4, 13.19, 16.53, 23.1, 27.6, 31.8, 40.8, 49.5, 58.8, 67.2, 76.7, 84.9, 94.1, 102.7]

'''plt.figure()
plt.plot(U3e, I3, color='blue')
plt.title("Kennlinie Diode (Sperrrichtung)")
plt.xlabel("Spannung U [V]")
plt.ylabel("Stromstärke I [mA]")
plt.grid(True)
plt.show()'''

# 4: Transistor
plt.figure()
plt.title("Kennlinien Transistor")
plt.xlabel("Spannung Uce [V]")
plt.ylabel("Stromstärke Ic [mA]")
plt.grid(True)

Uce1 = [0.1, 0.2, 0.3, 0.4, 0.6, 0.97, 1.3, 5, 10, 15.1, 20.1, 25.1, 30, 35.1, 40.2]
Ice1 = [4.5, 9.87, 9.89, 9.91, 9.92, 9.95, 10.0, 10.25, 10.5, 10.85, 11.2, 11.5, 11.8, 12.2, 12.5]
plt.plot(Uce1, Ice1, color='green', label='Ibe = 10 µA')

Uce2 = [0.1, 0.13, 0.136, 0.16, 0.2, 0.3, 0.4, 1, 5, 10, 15, 20, 25, 30, 35, 40]
Ice2 = [2.2, 3.75, 4.0, 4.95, 5.85, 6.6, 6.83, 6.9, 6.78, 7.1, 7.34, 7.68, 7.88, 8.1, 8.36, 8.6]
plt.plot(Uce2, Ice2, color='blue', label='Ibe = 20 µA')

Uce3 = [0.08, 0.111, 0.114, 0.14, 0.19, 0.25, 0.54, 0.84, 1.23, 4, 5, 4.5, 10, 20, 30, 40]
Ice3 = [2.0, 3.82, 4.09, 5.9, 7.85, 8.74, 10.3, 10.2, 9.8, 9.7, 9.9, 9.85, 10.3, 10.5, 10.9, 11.4]
plt.plot(Uce3, Ice3, color='red', label='Ibe = 30 µA')

Uce4 = [0.036, 0.047, 0.078, 0.12, 0.16, 0.2, 0.34, 0.6, 0.8, 0.95, 1.04, 1.5, 1.6, 1.7, 1.8, 2.0, 3.0, 4.3, 5.0, 10, 17, 23.6, 31.5, 40.3]
Ice4 = [0.44, 0.74, 2.27, 5.46, 8.2, 10.06, 11.76, 13.4, 13.5, 13.3, 13.0, 12.1, 12.1, 12.0, 12.0, 12.0, 12.0, 12.15, 12.3, 12.4, 12.75, 13.13, 13.4, 14.11]
plt.plot(Uce4, Ice4, color='gray', label='Ibe = 40 µA')

plt.legend()
#plt.show()
