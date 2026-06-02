import matplotlib.pyplot as plt
import streamlit as st

from waveguide_math import cutoff_frequency_rect, propagation_status, guide_wavelength, beta
from field_plotter import create_mode_figure

WAVEGUIDE_PRESETS = {
    "Custom": None,
    "WR-90": {"a_mm": 22.86, "b_mm": 10.16},
    "WR-62": {"a_mm": 15.80, "b_mm": 7.90},
    "WR-42": {"a_mm": 10.67, "b_mm": 4.32},
    "WR-28": {"a_mm": 7.11, "b_mm": 3.56},
}

MODE_PRESETS = {
    "Custom": None,
    "TE10": {"mode_type": "TE", "m": 1, "n": 0},
    "TE20": {"mode_type": "TE", "m": 2, "n": 0},
    "TE01": {"mode_type": "TE", "m": 0, "n": 1},
    "TE11": {"mode_type": "TE", "m": 1, "n": 1},
    "TM11": {"mode_type": "TM", "m": 1, "n": 1},
}

COMMON_MODES = [
    ("TE10", "TE", 1, 0),
    ("TE20", "TE", 2, 0),
    ("TE01", "TE", 0, 1),
    ("TE11", "TE", 1, 1),
    ("TM11", "TM", 1, 1),
]

st.set_page_config(page_title="Waveguide Mode Visualizer", layout="wide")

st.title("Waveguide Mode Visualizer")
st.caption("Rectangular waveguide TE and TM mode prototype")


def format_results_table(mode_label, status, fc_ghz, frequency_ghz, lambda_g_mm, beta_val):
    if lambda_g_mm is None:
        lambda_g_text = "N/A"
    else:
        lambda_g_text = f"{lambda_g_mm:.3f} mm"

    if beta_val is None:
        beta_text = "N/A"
    else:
        beta_text = f"{beta_val:.3f} rad/m"

    return f"""
| Quantity | Value |
|---|---|
| Mode | {mode_label} |
| Status | {status} |
| Cutoff frequency | {fc_ghz:.3f} GHz |
| Operating frequency | {frequency_ghz:.3f} GHz |
| Guide wavelength | {lambda_g_text} |
| Beta | {beta_text} |
"""


def create_cutoff_chart(a, b, eps_r, frequency_ghz):
    labels = []
    cutoffs = []

    for label, mode_type, m, n in COMMON_MODES:
        fc_hz = cutoff_frequency_rect(mode_type, a, b, m, n, eps_r=eps_r)
        labels.append(label)
        cutoffs.append(fc_hz / 1e9)

    order = sorted(range(len(cutoffs)), key=lambda i: cutoffs[i])
    labels = [labels[i] for i in order]
    cutoffs = [cutoffs[i] for i in order]

    fig, ax = plt.subplots(figsize=(8, 4))
    y_positions = list(range(len(labels)))

    ax.barh(y_positions, cutoffs)
    ax.axvline(frequency_ghz, linewidth=2)

    ax.set_yticks(y_positions)
    ax.set_yticklabels(labels)
    ax.set_xlabel("Cutoff frequency (GHz)")
    ax.set_title("Common Mode Cutoff Comparison")

    for i, cutoff in enumerate(cutoffs):
        ax.text(cutoff + 0.15, i, f"{cutoff:.3f} GHz", va="center")

    fig.tight_layout()
    return fig


def get_propagating_modes(a, b, eps_r, frequency_hz):
    active = []

    for label, mode_type, m, n in COMMON_MODES:
        fc_hz = cutoff_frequency_rect(mode_type, a, b, m, n, eps_r=eps_r)
        if frequency_hz > fc_hz:
            active.append(label)

    return active


with st.sidebar:
    st.header("Setup")

    waveguide_choice = st.selectbox(
        "Waveguide preset",
        list(WAVEGUIDE_PRESETS.keys()),
        index=1
    )

    if waveguide_choice == "Custom":
        a_mm = st.number_input(
            "Waveguide width a (mm)",
            min_value=0.001,
            value=22.86,
            step=0.01,
            format="%.3f"
        )
        b_mm = st.number_input(
            "Waveguide height b (mm)",
            min_value=0.001,
            value=10.16,
            step=0.01,
            format="%.3f"
        )
    else:
        a_mm = WAVEGUIDE_PRESETS[waveguide_choice]["a_mm"]
        b_mm = WAVEGUIDE_PRESETS[waveguide_choice]["b_mm"]
        st.info(f"{waveguide_choice}: a = {a_mm:.3f} mm, b = {b_mm:.3f} mm")

    mode_choice = st.selectbox(
        "Mode preset",
        list(MODE_PRESETS.keys()),
        index=1
    )

    if mode_choice == "Custom":
        mode_type = st.selectbox("Mode type", ["TE", "TM"])
        m = st.number_input("Mode number m", min_value=0, value=1, step=1)
        n = st.number_input("Mode number n", min_value=0, value=0, step=1)
    else:
        mode_type = MODE_PRESETS[mode_choice]["mode_type"]
        m = MODE_PRESETS[mode_choice]["m"]
        n = MODE_PRESETS[mode_choice]["n"]
        st.info(f"Selected mode: {mode_type}{m}{n}")

    eps_r = st.number_input(
        "Relative permittivity er",
        min_value=0.001,
        value=1.0,
        step=0.1,
        format="%.3f"
    )

    frequency_ghz = st.number_input(
        "Operating frequency (GHz)",
        min_value=0.001,
        value=10.0,
        step=0.1,
        format="%.3f"
    )

try:
    m = int(m)
    n = int(n)

    a = a_mm * 1e-3
    b = b_mm * 1e-3
    frequency_hz = frequency_ghz * 1e9

    fc = cutoff_frequency_rect(mode_type, a, b, m, n, eps_r=eps_r)
    status = propagation_status(frequency_hz, fc)
    lambda_g = guide_wavelength(frequency_hz, fc, eps_r=eps_r)
    beta_val = beta(frequency_hz, fc, eps_r=eps_r)

    if lambda_g is not None:
        lambda_g_mm = lambda_g * 1e3
    else:
        lambda_g_mm = None

    left_col, right_col = st.columns([1.0, 1.45])

    with left_col:
        st.subheader("Results")
        st.markdown(
            format_results_table(
                f"{mode_type}{m}{n}",
                status,
                fc / 1e9,
                frequency_ghz,
                lambda_g_mm,
                beta_val
            )
        )

        st.subheader("Input Summary")
        st.write(f"Waveguide width a: {a_mm:.3f} mm")
        st.write(f"Waveguide height b: {b_mm:.3f} mm")
        st.write(f"Relative permittivity er: {eps_r:.3f}")

        if status == "Propagating":
            st.success("Selected mode is above cutoff.")
        elif status == "At cutoff":
            st.warning("Selected mode is at cutoff.")
        else:
            st.error("Selected mode is below cutoff.")

        propagating_modes = get_propagating_modes(a, b, eps_r, frequency_hz)

        st.subheader("Common modes above cutoff")
        if propagating_modes:
            st.write(", ".join(propagating_modes))
        else:
            st.write("None")

        with st.expander("Quick demo cases"):
            st.write("WR-90 + TE10 + 10 GHz")
            st.write("WR-90 + TE20 + 10 GHz")
            st.write("WR-90 + TE11 + 20 GHz")
            st.write("WR-90 + TM11 + 20 GHz")

        st.write("")
        st.write("")

    with right_col:
        st.subheader("Field Plot")
        fig = create_mode_figure(a, b, mode_type, m, n)
        st.pyplot(fig, use_container_width=True)

        st.info(
            "How to read this plot\n\n"
            "Colors show the normalized longitudinal field component for the selected mode.\n\n"
            "Arrows show the relative direction of the transverse electric field in the waveguide cross section.\n\n"
            "Positive and negative color regions show field sign and variation across the guide.\n\n"
            "This is a normalized teaching plot, so it shows field shape and direction, not absolute field magnitude."
        )

    st.markdown("### Mode Cutoff Comparison")
    cutoff_fig = create_cutoff_chart(a, b, eps_r, frequency_ghz)
    st.pyplot(cutoff_fig, use_container_width=True)

except ValueError as e:
    st.error(f"Input error: {e}")