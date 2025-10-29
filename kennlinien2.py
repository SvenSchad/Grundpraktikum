import matplotlib.pyplot as plt  # plot
import numpy as np
from scipy.optimize import curve_fit
import uncertainties.unumpy as unp

U1_ERR = 0.01
I1_ERR = 0.01 * 1e-3
U1 = unp.uarray(
    np.array(range(2, 82, 2)),
    U1_ERR,
)

I = (
    np.array(
        [
            1.04,
            2.17,
            3.26,
            4.33,
            5.47,
            6.60,
            7.77,
            8.89,
            10.09,
            11.23,
            12.47,
            13.67,
            14.86,
            16.13,
            17.40,
            18.64,
            19.90,
            21.4,
            22.7,
            24.0,
            25.4,
            26.8,
            28.1,
            29.5,
            30.9,
            32.3,
            33.7,
            35.1,
            36.5,
            37.9,
            39.4,
            40.8,
            42.3,
            43.4,
            45.3,
            46.8,
            48.4,
            50.0,
            51.6,
            53.2,
        ]
    )
    * 1e-3
)
I1 = unp.uarray(I, I1_ERR)

# 1: Darstellung (I,U) Wertepaar
plt.figure()
plt.errorbar(
    unp.nominal_values(U1),
    unp.nominal_values(I1),
    xerr=U1_ERR,
    yerr=I1_ERR,
    color="red",
    fmt="o--",
    ecolor="black",
    capsize=3,
)
plt.grid(True)
plt.title("Kennlinie Kohlefadenlampe")
plt.xlabel("Spannung U [V]")
plt.ylabel("Stromstärke I [A]")
plt.show()
# 2: Leistung gegen relativie Widerstandsänderung doppelt logarithmisch
P = U1 * I1
P_cut = P[1:]
R = U1 / I1
r = R / R[0] - 1  # Das ist schwurbel and yk it bitch not anymore tho wuuuu


# Stefan-Boltzmann-Gesetz nichtlinear an Messdaten
def stefan_boltzmann(r, A, c):
    sigma = 5.67e-8
    T0 = 293  # 20 Grad Celsius
    dT = -r / c
    return sigma * A * ((T0 + dT) ** 4 - T0**4)


# fitter als ein Turnschuh
popt, pcov = curve_fit(
    stefan_boltzmann,  # Fit fkt
    unp.nominal_values(r),  # r
    unp.nominal_values(P),  # P
    sigma=unp.std_devs(P),  # y-Fehler
    absolute_sigma=True,  # Gewichtung Fehler
    p0=[1e-5, 4.5e-3],  # Startwerte für c &  (pun intended) laut ChadGpt so gut idk why
    maxfev=200000,  # I do not want ze runtime error
)

A_fit = popt[0]
A_err = np.sqrt(np.diag(pcov))[0]
c_fit = popt[1]
c_err = np.sqrt(np.diag(pcov))[1]

r_cut = r[1:]
# Plitz und Plotter
r_fit = np.linspace(min(unp.nominal_values(r_cut)), max(unp.nominal_values(r)), 200)
P_fit = stefan_boltzmann(r_fit, A_fit, c_fit)
plt.figure()
plt.errorbar(
    unp.nominal_values(r),
    unp.nominal_values(P),
    xerr=unp.std_devs(r),
    yerr=unp.std_devs(P),
    fmt="o",
    color="dodgerblue",
    ecolor="black",
    capsize=3,
    label="Messwerte",
    zorder=1,
)
plt.plot(
    r_fit,
    P_fit,
    color="orange",
    label="Stefan-Bolzmann-ist-fit",
    zorder=2,  # das wird als zweites geplottet das es schöner aussieht sehr wichtig
)
plt.xscale("symlog")
plt.yscale("symlog")
plt.xlabel("relative Widerstandsänderung r")
plt.ylabel("Leistung P [W]")
plt.title("Fit des Stefan-Boltzmann-Gesetzes")
plt.grid(True, which="both", linestyle="--", alpha=0.7)
plt.legend()
plt.show()

print(f"Gefittete Fläche A = {A_fit:.3e} +- {A_err:.3e} m²")
print(f"Gefitteter Wärmekoeffi oder so c = {c_fit:.3e} +- {c_err:.3e}")

# 3:Temperaturen
c = unp.uarray(c_fit, c_err)
T = r_cut / c
plt.figure()
plt.errorbar(
    unp.nominal_values(T),
    unp.nominal_values(P_cut),
    xerr=unp.std_devs(T),
    yerr=unp.std_devs(P_cut),
    fmt="o--",
    color="dodgerblue",
    ecolor="black",
    capsize=3,
    label="Leistung vs Temp",
)
plt.xscale("symlog")
plt.yscale("symlog")
plt.xlabel("Temperaturänderung dT [K]")
plt.ylabel("Leistung P [W]")
plt.title("Temperatur bei Leistung")
plt.grid(True, which="both", linestyle="--", alpha=0.7)
plt.legend()
plt.show()

# Berechnung Drahtlänge L, Drahtradius x
rho_kohlefaden = 2e-5
A = unp.uarray(A_fit, A_err)
x = np.power((rho_kohlefaden * A / (R[0] * 2 * np.pi**2)), 1 / 3)
L = A / (2 * np.pi * x)
print(f"Drahtradius = {unp.nominal_values(x):.3e} +- {unp.std_devs(x):.3e} m²")
print(f"Drahtlänge = {unp.nominal_values(L):.3e} +- {unp.std_devs(L):.3e} m²")
