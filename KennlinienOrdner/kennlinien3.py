# Part two Diode
import matplotlib.pyplot as plt
import numpy as np
import uncertainties.unumpy as unp

U_ERR = 0.01
I_ERR = 0.01 * 1e-3
U_DURCH = unp.uarray(np.array([0.51, 0.616, 0.642, 0.706, 0.744, 0.746]), U_ERR)
I_DURCH = unp.uarray(np.array([0.01, 0.565, 1.535, 18.36, 82.0, 92.0]) * 1e-3, I_ERR)
U_SPERR = unp.uarray(
    np.array(
        [
            1.35,
            2.23,
            3.53,
            4.47,
            5.00,
            5.33,
            5.40,
            5.41,
            5.43,
            5.44,
            5.45,
            5.46,
            5.47,
            5.48,
        ]
    ),
    U_ERR,
)
I_SPERR = unp.uarray(
    np.array(
        [0.1, 0.2, 0.4, 0.6, 0.8, 1.2, 2.0, 6.6, 18.1, 30.8, 41.5, 60.5, 81.6, 96.0]
    ),
    I_ERR,
)


def kennlinie(u, i, name):
    """bla bal bla"""
    plt.figure()
    plt.errorbar(
        unp.nominal_values(u),
        unp.nominal_values(i),
        fmt="o--",
        color="dodgerblue",
        ecolor="black",
        capsize=3,
        label="Messwerte",
        zorder=1,
        xerr=unp.std_devs(u),
        yerr=unp.std_devs(i),
    )
    plt.xlabel("Spannung U [V]")
    plt.ylabel("Stromstärke I [A]")
    plt.title(f"Kennlinie {name}")
    plt.grid(True, which="both", linestyle="--", alpha=0.7)
    # Verlustleistungshyperbel
    p_max = max(unp.nominal_values(u)) * max(unp.nominal_values(i))
    i_vals = p_max / unp.nominal_values(u)
    plt.plot(
        unp.nominal_values(u),
        i_vals,
        color="red",
        linestyle="--",
        label=f"Verlustleistungshyperbel (P_Max = {p_max:.2f} W)",
    )
    plt.legend()
    plt.show()
    plt.figure()
    plt.errorbar(
        unp.nominal_values(u),
        unp.nominal_values(i),
        xerr=unp.std_devs(u),
        yerr=unp.std_devs(i),
    )
    plt.xlabel("Spannung U [V]")
    plt.ylabel("Stromstärke log(I) [A]")
    plt.title(f"Halblogarithmischer Plot der {name}")
    plt.yscale("log")
    plt.grid(True)
    plt.show()


kennlinie(U_DURCH, I_DURCH, "Durchlassdiode")
kennlinie(U_SPERR, I_SPERR, "Sperrdiode")
