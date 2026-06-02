import numpy as np
import matplotlib.pyplot as plt


def te_mode_patterns(a: float, b: float, m: int, n: int, nx: int = 140, ny: int = 100):
    x = np.linspace(0.0, a, nx)
    y = np.linspace(0.0, b, ny)
    X, Y = np.meshgrid(x, y)

    mx = m * np.pi * X / a
    ny_term = n * np.pi * Y / b

    Hz = np.cos(mx) * np.cos(ny_term)

    Ex = -(n * np.pi / b) * np.cos(mx) * np.sin(ny_term) if n != 0 else np.zeros_like(Hz)
    Ey = +(m * np.pi / a) * np.sin(mx) * np.cos(ny_term) if m != 0 else np.zeros_like(Hz)

    return X, Y, Hz, Ex, Ey, "Normalized $H_z$"


def tm_mode_patterns(a: float, b: float, m: int, n: int, nx: int = 140, ny: int = 100):
    x = np.linspace(0.0, a, nx)
    y = np.linspace(0.0, b, ny)
    X, Y = np.meshgrid(x, y)

    mx = m * np.pi * X / a
    ny_term = n * np.pi * Y / b

    Ez = np.sin(mx) * np.sin(ny_term)

    Ex = -(m * np.pi / a) * np.cos(mx) * np.sin(ny_term)
    Ey = -(n * np.pi / b) * np.sin(mx) * np.cos(ny_term)

    return X, Y, Ez, Ex, Ey, "Normalized $E_z$"


def normalize_pattern(scalar_field, Ex, Ey):
    scalar_max = np.max(np.abs(scalar_field))
    if scalar_max > 0:
        scalar_field = scalar_field / scalar_max

    mag = np.sqrt(Ex**2 + Ey**2)
    mag_max = np.max(mag)
    if mag_max > 0:
        Ex = Ex / mag_max
        Ey = Ey / mag_max

    return scalar_field, Ex, Ey


def create_mode_figure(a: float, b: float, mode_type: str, m: int, n: int):
    mode_type = mode_type.upper()

    if mode_type == "TE":
        X, Y, scalar_field, Ex, Ey, colorbar_label = te_mode_patterns(a, b, m, n)
    elif mode_type == "TM":
        X, Y, scalar_field, Ex, Ey, colorbar_label = tm_mode_patterns(a, b, m, n)
    else:
        raise ValueError("Mode type must be TE or TM.")

    scalar_field, Ex, Ey = normalize_pattern(scalar_field, Ex, Ey)

    fig, ax = plt.subplots(figsize=(9, 4.5))

    levels = np.linspace(-1, 1, 21)
    contour = ax.contourf(X * 1e3, Y * 1e3, scalar_field, levels=levels)
    fig.colorbar(contour, ax=ax, label=colorbar_label)

    step_y = max(1, Y.shape[0] // 14)
    step_x = max(1, X.shape[1] // 18)

    ax.quiver(
        X[::step_y, ::step_x] * 1e3,
        Y[::step_y, ::step_x] * 1e3,
        Ex[::step_y, ::step_x],
        Ey[::step_y, ::step_x],
        pivot="mid",
        scale=12
    )

    ax.set_title(f"Rectangular Waveguide {mode_type}{m}{n} Mode Pattern")
    ax.set_xlabel("x (mm)")
    ax.set_ylabel("y (mm)")
    ax.set_aspect("equal")
    ax.set_xlim(0, a * 1e3)
    ax.set_ylim(0, b * 1e3)

    for spine in ax.spines.values():
        spine.set_linewidth(1.2)

    fig.tight_layout()
    return fig