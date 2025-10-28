# Part two Diode
import matplotlib.pyplot as plt
import numpy as np
import uncertainties.unumpy as unp

U_ERR = 0.01
I_ERR = 0.01 * 1e-3
U_DURCH = unp.uarray(np.array([0.51, 0.616, 0.642, 0.706, 0.744, 0.746]), U_ERR)
I_DURCH = unp.uarray(np.array([0.01, 0.565, 1.535, 18.36, 82.0, 92.0]) * 1e-3, I_ERR)


def kennlinie(U, I, name):
    plt.figure()
    plt.errorbar(
        unp.nominal_values(U),
        unp.nominal_values(I),
        fmt="o--",
        color="dodgerblue",
        ecolor="black",
        capsize=3,
        label="Messwerte",
        zorder=1,
        xerr=unp.std_devs(U),
        yerr=unp.std_devs(I),
    )
    plt.xlabel("Spannung U [V]")
    plt.ylabel("Stromstärke I [A]")
    plt.title(f"Kennlinie {name}")
    plt.grid(True, which="both", linestyle="--", alpha=0.7)
    plt.show()


kennlinie(U_DURCH, I_DURCH, "Durchlassdiode")
