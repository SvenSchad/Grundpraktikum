# Spannungsstab
import matplotlib.pyplot as plt
import numpy as np
from uncertainties import unumpy as unp

U_ERR = 0.01
Ue = unp.uarray(
    np.array(
        [
            0,
            0.5,
            1.0,
            1.5,
            2.0,
            2.5,
            3.0,
            3.5,
            4,
            5,
            5.5,
            6.0,
            6.5,
            7.0,
            7.5,
            8.0,
            8.5,
            9.0,
            10,
            11,
            12,
            13,
            14,
            15,
            16,
            17,
        ]
    ),
    U_ERR,
)
Ua = unp.uarray(
    np.array(
        [
            0.1,
            0.61,
            1.1,
            1.57,
            2.06,
            2.57,
            3.07,
            3.6,
            4.1,
            5.08,
            5.5,
            5.53,
            5.53,
            5.54,
            5.54,
            5.55,
            5.55,
            5.55,
            5.56,
            5.56,
            5.57,
            5.57,
            5.58,
            5.58,
            5.59,
            5.59,
        ]
    ),
    U_ERR,
)


def quatsch(ue, ua):
    """bla bal bla"""
    plt.plot(unp.nominal_values(ue), unp.nominal_values(ua), "o-", label="Messwerte")
    # Glättungsfaktor im stabilisierten Bereich
    ue_cut = unp.nominal_values(ue[12:])
    ua_cut = unp.nominal_values(ua[12:])
    g, c = np.polyfit(ue_cut, ua_cut, 1)
    x_fit = np.linspace(ue_cut[0], ue_cut[-1], 1000)

    y_fit = g * x_fit + c
    plt.plot(
        x_fit,
        y_fit,
        "--",
        color="red",
        label = f"Steigung des Linearen Fits G = {g:.4f}"
    )
    plt.xlabel("Eingangsspannung Ue [V]")
    plt.ylabel("Ausgangsspannung Ua [V]")
    plt.title("Spannungsstabilisierung mit Zener-Diode")
    plt.grid(True)
    plt.legend()
    plt.show()

quatsch(Ue, Ua)
