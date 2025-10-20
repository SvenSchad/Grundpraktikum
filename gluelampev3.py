import matplotlib.pyplot as plt #plot
import numpy as np
from scipy.optimize import curve_fit
import uncertainties.unumpy as unp

U1_ERR = 0.01
I1_ERR = 0.01 * 1e-3
U1 = unp.uarray(
    [
        2.04,
        3.88,
        6.07,
        8.01,
        10.02,
        12.00,
        14.02,
        15.93,
        17.96,
        19.87,
        21.9,
        23.8,
        25.8,
        27.8,
        29.8,
        31.7,
        33.7,
        35.9,
        37.8,
        39.8,
        41.9,
        43.9,
        45.9,
        47.9,
        49.9,
        51.9,
        53.8,
        55.8,
        57.8,
        59.8,
        61.7,
        63.7,
        65.8,
        67.9,
        69.8,
        71.7,
        73.8,
        75.9,
        78,
        80.1,
    ],
    U1_ERR,
)
I = (
    np.array(
        [
            1.035,
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
            16.10,
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
            38.4,
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
plt.title("Kennlinie Glühlampe")
plt.xlabel("Spannung U [V]")
plt.ylabel("Stromstärke I [A]")
plt.show()
# 2: Leistung gegen relativie Widerstandsänderung doppelt logarithmisch
P = U1 * I1
R = U1 / I1
r = -(R / R[0] - 1) #Das ist schwurbel and yk it bitch

plt.figure()
plt.errorbar(
    unp.nominal_values(P),
    unp.nominal_values(r),
    xerr=unp.std_devs(P),
    yerr=unp.std_devs(r),
    fmt='o--',
    color='green',
    ecolor='black',
    capsize=3
)
plt.xscale('log')
plt.yscale('log')
plt.grid(True, which='both')
plt.title("relative Widerstandsänderung bei Leistung")
plt.xlabel("Leistung P [W]")
plt.ylabel("relative Widerstandsänderung r")
plt.show()

#3: Stefan-Boltzmann-Gesetz nichtlinear an Messdaten
def stefan_boltzmann(r, c, A):
    sigma = 5.67e-8
    T0 = 293 # 20 Grad Celsius
    dT = r/c
    return sigma*A*((T0+dT)**4-T0**4)

#fitter als ein Turnschuh
#startwerte:
popt, pcov = curve_fit(
    stefan_boltzmann, #Fit fkt
    unp.nominal_values(r), #r
    unp.nominal_values(P), #P
    sigma=unp.std_devs(P), #y-Fehler
    absolute_sigma=True,   #Gewichtung Fehler
    p0=[0.005, 0.01],         #Startwert für c & A (pun intended) laut ChadGpt so gut idk why
    maxfev=100000           # I do not want ze runtime error
)

c_fit, A_fit = popt
c_err, A_err = np.sqrt(np.diag(pcov))
print(f"Gefitteter c-Wert: {c_fit:.4f} ± {c_err:.4f}")
print(f"Gefitteter A-Wert: {A_fit:.4f} ± {A_err:.4f}")
#Plitz und Plotter
r_fit = np.linspace(min(unp.nominal_values(r)), max(unp.nominal_values(r)), 1000)
P_fit = stefan_boltzmann(r_fit, c_fit, A_fit)
plt.figure()
plt.errorbar(
    unp.nominal_values(r),
    unp.nominal_values(P),
    xerr=unp.std_devs(r),
    yerr=unp.std_devs(P),
    fmt='o',
    color='dodgerblue',
    ecolor='black',
    capsize=3,
    label='Messwerte',
    zorder = 1
)
plt.plot(
    r_fit,
    P_fit,
    color='orange',
    label='Stefan-Bolzmann-ist-fit',
    zorder=2    #das wird als zweites geplottet das es schöner aussieht sehr wichtig
)
plt.xlabel("relative Widerstandsänderung r")
plt.ylabel("Leistung P [W]")
plt.title("Fit des Stefan-Boltzmann-Gesetzes")
plt.grid(True, which='both', linestyle='--', alpha=0.7)
plt.legend()
plt.show()

#4:Temperaturen