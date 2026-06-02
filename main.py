from waveguide_math import cutoff_frequency_rect, propagation_status, guide_wavelength, beta
from field_plotter import plot_mode


def main():
    print("Waveguide Mode Visualizer - Prototype V3")
    print("----------------------------------------")

    try:
        mode_type = input("Enter mode type (TE or TM): ").strip().upper()
        a_mm = float(input("Enter waveguide width a (mm): "))
        b_mm = float(input("Enter waveguide height b (mm): "))
        eps_r = float(input("Enter relative permittivity er (use 1 for air): "))
        m = int(input("Enter mode number m: "))
        n = int(input("Enter mode number n: "))
        frequency_ghz = float(input("Enter operating frequency (GHz): "))

        a = a_mm * 1e-3
        b = b_mm * 1e-3
        frequency_hz = frequency_ghz * 1e9

        fc = cutoff_frequency_rect(mode_type, a, b, m, n, eps_r=eps_r)
        status = propagation_status(frequency_hz, fc)
        lambda_g = guide_wavelength(frequency_hz, fc, eps_r=eps_r)
        beta_val = beta(frequency_hz, fc, eps_r=eps_r)

        print("\nResults")
        print("-------")
        print(f"Mode                = {mode_type}{m}{n}")
        print(f"a                   = {a_mm:.3f} mm")
        print(f"b                   = {b_mm:.3f} mm")
        print(f"er                  = {eps_r:.3f}")
        print(f"Operating frequency = {frequency_hz / 1e9:.3f} GHz")
        print(f"Cutoff frequency    = {fc / 1e9:.3f} GHz")
        print(f"Status              = {status}")

        if lambda_g is not None:
            print(f"Guide wavelength    = {lambda_g * 1e3:.3f} mm")
        else:
            print("Guide wavelength    = N/A")

        if beta_val is not None:
            print(f"Beta                = {beta_val:.3f} rad/m")
        else:
            print("Beta                = N/A")

        plot_mode(a, b, mode_type, m, n)

    except ValueError as e:
        print(f"\nInput error: {e}")


if __name__ == "__main__":
    main()