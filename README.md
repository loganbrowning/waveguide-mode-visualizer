# Waveguide Mode Visualizer

A Python-based rectangular waveguide mode visualizer built for ECE 3323 Electromagnetics II at Mississippi State University.

This project lets a user select waveguide dimensions, material properties, operating frequency, and TE/TM mode numbers. The program calculates cutoff frequency, checks whether the selected mode propagates, calculates guide wavelength and beta, and displays a field plot for the selected mode.

## Features

* Rectangular waveguide TE and TM mode support
* Cutoff frequency calculation
* Propagation status check
* Guide wavelength calculation
* Propagation constant beta calculation
* Normalized field pattern visualization
* Streamlit web interface
* Waveguide and mode presets
* Cutoff comparison chart for common modes

## Tools Used

* Python
* NumPy
* Matplotlib
* Streamlit
* PyCharm

## How to Run

Install the required packages:

```bash
pip install -r requirements.txt
```

Run the Streamlit app:

```bash
python -m streamlit run app.py
```

## Example Demo Case

Example setup:

```text
Waveguide: WR-90
Mode: TE10
Frequency: 10 GHz
Relative permittivity: 1
```

Expected result:

```text
Cutoff frequency: about 6.557 GHz
Status: Propagating
```

## Project Purpose

Rectangular waveguide modes can be difficult to understand from equations alone. This project connects the electromagnetic theory to a visual tool so the user can see how mode selection, frequency, and waveguide dimensions affect propagation and field patterns.

## Repository Structure

```text
waveguide-mode-visualizer/
├── app.py
├── main.py
├── field_plotter.py
├── waveguide_math.py
├── requirements.txt
└── README.md
```

## Author

Logan Browning
Electrical Engineering Student
Mississippi State University
