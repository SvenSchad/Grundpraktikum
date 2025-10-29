# Transistooooooooor Ronaldooooo
import matplotlib.pyplot as plt
import numpy as np


U_ERR = 0.01
I_ERR = 0.01 * 1e-3

I_BE1 = 10e-6  # mykro amp
U_CE1 = np.array(
    [0.1, 0.2, 0.3, 0.4, 0.6, 0.97, 1.3, 5, 10, 15.1, 20.1, 25.1, 30, 35.1, 40.2]
)
I_CE1 = np.array(
        [
            4.5,
            9.87,
            9.89,
            9.91,
            9.92,
            9.95,
            10.0,
            10.25,
            10.5,
            10.85,
            11.2,
            11.5,
            11.8,
            12.2,
            12.6,
        ]
    )* 1e-3

I_BE2 = 20e-6
U_CE2 = np.array(
    [0.1, 0.13, 0.136, 0.16, 0.2, 0.3, 0.4, 1, 5, 10, 15, 20, 25, 30, 35, 40]
)
I_CE2 = np.array(
        [
            2.2,
            3.75,
            4.0,
            4.95,
            5.85,
            6.6,
            6.83,
            6.9,
            6.78,
            7.1,
            7.34,
            7.68,
            7.88,
            8.1,
            8.36,
            8.6,
        ]
    )* 1e-3


I_BE3 = 30e-6
U_CE3 = np.array(
    [
        0.08,
        0.111,
        0.114,
        0.14,
        0.19,
        0.25,
        0.54,
        0.84,
        1.23,
        4,
        4.5,
        5,
        10,
        20,
        30,
        40,
    ]
)
I_CE3 = np.array(
        [
            2.0,
            3.82,
            4.09,
            5.9,
            7.85,
            8.74,
            10.3,
            10.2,
            9.8,
            9.7,
            9.85,
            9.95,
            10.3,
            10.5,
            10.9,
            11.4,
        ]
    )* 1e-3


I_BE4 = 40e-6
U_CE4 = np.array(
        [
            0,
            0.036,
            0.047,
            0.078,
            0.12,
            0.16,
            0.2,
            0.34,
            0.6,
            0.804,
            0.9,
            0.95,
            1.04,
            1.54,
            1.6,
            1.7,
            1.82,
            2.0,
            3.05,
            4.3,
            5.07,
            10.25,
            17.15,
            23.6,
            31.5,
            40,
        ]
    )
I_CE4 = np.array(
        [
            0,
            0.44,
            0.74,
            2.27,
            5.46,
            8.22,
            10.06,
            11.76,
            13.48,
            13.57,
            13.42,
            13.29,
            13.02,
            12.15,
            12.1,
            12.02,
            11.96,
            11.96,
            11.97,
            12.15,
            12.32,
            12.46,
            12.81,
            13.10,
            13.46,
            14.13,
        ]
    )* 1e-3


def schabernack(u_ce, i_ce, i_be, color, zahl):
    """bla"""
    plt.plot(
        u_ce,
        i_ce,
        "o",
        ls="-",
        markersize=4,
        label=f"I_BE = {i_be*1e6} μA",
        color=f"{color}",
    )
    u_mask = u_ce > 1.6
    u_ce = u_ce[u_mask]
    i_ce = i_ce[u_mask]
    p, cov = np.polyfit(u_ce, i_ce, 1, cov=True)
    m,c = p
    c_err = np.sqrt(np.diag(cov))

    x_fit = np.linspace(u_ce[0], u_ce[-1], 1000)
    y_fit = m * x_fit + c
    plt.plot(
        x_fit,
        y_fit,
        "--",
        color="black",
        label=f"Steigung m = {m:.3e} ± {c_err[0]:.3e})",
    )
    plt.xlabel("Connector Emittor Spannung [V]")
    plt.ylabel("Connector Emittor Stromstärke [A]")
    plt.title("Kennlinienschaar")
    plt.grid(True)
    plt.legend()
    print(f"r_CE{zahl}={m**(-1):.3e} [Ohm]")


schabernack(U_CE1, I_CE1, I_BE1, "green", 1)
schabernack(U_CE2, I_CE2, I_BE2, "red", 2)
schabernack(U_CE3, I_CE3, I_BE3, "orange", 3)
schabernack(U_CE4, I_CE4, I_BE4, "blue", 4)
plt.show()
