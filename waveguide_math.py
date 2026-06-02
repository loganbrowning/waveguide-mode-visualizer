import math
from typing import Optional

C0 = 299_792_458.0
MU0 = 4 * math.pi * 1e-7
EPS0 = 8.854187817e-12


def validate_mode(mode_type: str, m: int, n: int) -> None:
    mode_type = mode_type.upper()

    if m < 0 or n < 0:
        raise ValueError("Mode numbers m and n must be nonnegative integers.")

    if mode_type == "TE":
        if m == 0 and n == 0:
            raise ValueError("TE00 is not a valid rectangular waveguide mode.")
    elif mode_type == "TM":
        if m == 0 or n == 0:
            raise ValueError("TM modes require m > 0 and n > 0.")
    else:
        raise ValueError("Mode type must be TE or TM.")


def cutoff_frequency_rect(mode_type: str, a: float, b: float, m: int, n: int,
                          eps_r: float = 1.0, mu_r: float = 1.0) -> float:
    """
    Cutoff frequency for rectangular waveguide TE_mn or TM_mn mode.

    a, b in meters
    eps_r = relative permittivity
    mu_r = relative permeability
    returns fc in Hz
    """
    if a <= 0 or b <= 0:
        raise ValueError("Waveguide dimensions must be positive.")
    if eps_r <= 0 or mu_r <= 0:
        raise ValueError("eps_r and mu_r must be positive.")

    validate_mode(mode_type, m, n)

    v = C0 / math.sqrt(eps_r * mu_r)
    fc = (v / 2.0) * math.sqrt((m / a) ** 2 + (n / b) ** 2)
    return fc


def propagation_status(frequency_hz: float, fc_hz: float) -> str:
    if frequency_hz > fc_hz:
        return "Propagating"
    if math.isclose(frequency_hz, fc_hz, rel_tol=1e-9, abs_tol=1e-12):
        return "At cutoff"
    return "Below cutoff / evanescent"


def guide_wavelength(frequency_hz: float, fc_hz: float,
                     eps_r: float = 1.0, mu_r: float = 1.0) -> Optional[float]:
    """
    Returns guide wavelength in meters if propagating, otherwise None.
    """
    if frequency_hz <= fc_hz:
        return None

    lambda_medium = C0 / (frequency_hz * math.sqrt(eps_r * mu_r))
    return lambda_medium / math.sqrt(1.0 - (fc_hz / frequency_hz) ** 2)


def beta(frequency_hz: float, fc_hz: float,
         eps_r: float = 1.0, mu_r: float = 1.0) -> Optional[float]:
    """
    Phase constant beta in rad/m if propagating, otherwise None.
    """
    if frequency_hz <= fc_hz:
        return None

    k = 2.0 * math.pi * frequency_hz * math.sqrt(eps_r * mu_r) / C0
    return k * math.sqrt(1.0 - (fc_hz / frequency_hz) ** 2)