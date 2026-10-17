# The Ocean Descent: Exploring Challenger Deep

An interactive Streamlit pages for exploring the ocean's deepest known region, Challenger Deep in the Mariana Trench with real scientific data.

## Overview

The ocean-depth information through an interactive application, combining scientific data with visual exploration. It makes the depth and bathymetry of Challenger Deep easier to explore.

## Features

- **Ocean Descent:** Depth information through an interactive interface.
- **Bathymetry:** Visualize underwater topography.
- **Data & Methods:** Review the data and methods used.


## Getting Started

### Requirements

- Python
- Streamlit
- NumPy and Pandas
- SciPy and h5py
- Plotly
- Git
- The project files and scientific data included in this repository

### Installation

Clone repository:

```bash
git clone https://github.com/shyam-ocean/Ocean_Descent_Challengerdeep.git
cd Ocean_Descent_Challengerdeep
```

Installing requiremnets:

```bash
python -m pip install -r requirements.txt
```

### Run the application

Start the Streamlit app:

```bash
python -m streamlit run app.py
```

Streamlit local URL in the terminal, `http://localhost:8501`. Open URL in your browser to explore Ocean Decent.

## Project Structure

- `app.py` : Main application entry point
- `ui.py` :User interface components
- `depth_information.py` : Depth information
- `pages/` : Pages
- `Challenger_Deep_Extracted_Data/` :Scientific data used
- `requirements.txt` : Requirements

## Data and Acknowledgements

This project uses scientific data associated with the following research publication:
Huichang Jiang. (2024). Three-layer circulation in the world deepest trench [Dataset]. Zenodo. https://doi.org/10.5281/zenodo.13870930

## Author

This is an educational and visualization work exploring Challenger Deep. Displayed values and visualizations should be interpreted according to the source data and the methodological notes provided. 
Illustrative visual effects are not direct scientific observations.
