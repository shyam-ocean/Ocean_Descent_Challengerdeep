import os
import zipfile
import shutil

import numpy as np
import pandas as pd
import h5py
from scipy.io import savemat


# ============================================================
# SETTINGS
# ============================================================

ZIP_FILE = "Trial/SourceData.zip"

OUTPUT_FOLDER = "Trial/Challenger_Deep_Extracted_Data"

# Files inside the Nature/Zenodo SourceData.zip
CTD_FILE = "SourceData/Data_Availability/FigureS6_2.mat"
BATHY_FILE = "SourceData/Data_Availability/FigureS6_1.mat"
MODEL_FIG6_FILE = "SourceData/Data_Availability/Figure6.mat"
MODEL_FIG7_FILE = "SourceData/Data_Availability/Figure7_1.mat"


# ============================================================
# CREATE TEMPORARY EXTRACTION FOLDER
# ============================================================

TEMP_FOLDER = "_temp_challenger_data"

if os.path.exists(TEMP_FOLDER):
    shutil.rmtree(TEMP_FOLDER)

os.makedirs(TEMP_FOLDER)


# ============================================================
# CHECK ZIP
# ============================================================

if not os.path.exists(ZIP_FILE):
    raise FileNotFoundError(
        f"\nCould not find '{ZIP_FILE}'.\n"
        "Put SourceData.zip in the same folder as this Python script."
    )


print("\nOpening SourceData.zip...")


# ============================================================
# EXTRACT ONLY THE FILES WE NEED
# ============================================================

with zipfile.ZipFile(ZIP_FILE, "r") as z:

    all_files = z.namelist()

    required_files = [
        CTD_FILE,
        BATHY_FILE,
        MODEL_FIG6_FILE,
        MODEL_FIG7_FILE
    ]

    for file in required_files:

        if file in all_files:

            print("Extracting:", file)

            z.extract(file, TEMP_FOLDER)

        else:

            print("WARNING: File not found:", file)


# ============================================================
# FUNCTION TO READ MATLAB v7.3 FILES
# ============================================================

def read_matlab_v73(filename):

    """
    Reads numeric variables from MATLAB v7.3 (.mat)
    files using HDF5.

    MATLAB v7.3 files are internally HDF5 files.
    """

    data = {}

    print("\nReading:", filename)

    with h5py.File(filename, "r") as f:

        def visitor(name, obj):

            if not isinstance(obj, h5py.Dataset):
                return

            # Ignore MATLAB object references
            if h5py.check_dtype(ref=obj.dtype) is not None:
                return

            # Only numeric datasets
            if obj.dtype.kind not in "biufc":
                return

            array = np.array(obj)

            # MATLAB uses column-major ordering.
            # Transpose multidimensional arrays.
            if array.ndim > 1:
                array = array.T

            variable_name = name.split("/")[-1]

            data[variable_name] = array

        f.visititems(visitor)

    return data


# ============================================================
# FUNCTION TO SAVE CSV
# ============================================================

def save_csv(variable_name, array, folder):

    array = np.asarray(array)

    filename = os.path.join(
        folder,
        variable_name + ".csv"
    )

    # 1D
    if array.ndim == 1:

        df = pd.DataFrame({
            variable_name: array
        })

        df.to_csv(filename, index=False)

    # 2D
    elif array.ndim == 2:

        df = pd.DataFrame(array)

        df.to_csv(filename, index=False)

    # 3D or higher
    else:

        print(
            f"  Converting {variable_name} "
            f"{array.shape} to long-format CSV..."
        )

        indices = np.indices(array.shape)

        indices = indices.reshape(
            array.ndim,
            -1
        ).T

        columns = []

        for i in range(array.ndim):
            columns.append(f"dim{i + 1}")

        df = pd.DataFrame(
            indices,
            columns=columns
        )

        df["value"] = array.reshape(-1)

        df.to_csv(
            filename,
            index=False
        )

    return filename


# ============================================================
# CREATE OUTPUT DIRECTORIES
# ============================================================

CTD_FOLDER = os.path.join(
    OUTPUT_FOLDER,
    "01_Full_Depth_CTD_Profile"
)

BATHY_FOLDER = os.path.join(
    OUTPUT_FOLDER,
    "02_Bathymetry_and_Vertical_Grid"
)

FIG6_FOLDER = os.path.join(
    OUTPUT_FOLDER,
    "03_Model_Temp_Sal_Density_Figure6"
)

FIG7_FOLDER = os.path.join(
    OUTPUT_FOLDER,
    "04_Model_Temp_Sal_Density_Figure7_1"
)


for folder in [
    CTD_FOLDER,
    BATHY_FOLDER,
    FIG6_FOLDER,
    FIG7_FOLDER
]:

    os.makedirs(
        folder,
        exist_ok=True
    )


# ============================================================
# 1. FULL-DEPTH CTD
# ============================================================

print("\n" + "=" * 60)
print("1. FULL-DEPTH CHALLENGER DEEP CTD")
print("=" * 60)


ctd_path = os.path.join(
    TEMP_FOLDER,
    CTD_FILE
)

ctd = read_matlab_v73(ctd_path)


print("\nVariables found:")

for key in ctd:
    print(
        f"  {key}: "
        f"{np.asarray(ctd[key]).shape}"
    )


# Original variables
depth = np.asarray(
    ctd["depth2"]
).squeeze().astype(float)

salinity = np.asarray(
    ctd["salt2"]
).squeeze().astype(float)

potential_temperature = np.asarray(
    ctd["ptmp2"]
).squeeze().astype(float)

sigma8 = np.asarray(
    ctd["rho8"]
).squeeze().astype(float)


# ------------------------------------------------------------
# Convert depth
# ------------------------------------------------------------

# Source data use negative depth.
#
# Example:
# -5000 m -> 5000 m
#
depth_positive = -depth


# ------------------------------------------------------------
# Calculate absolute potential density
# ------------------------------------------------------------

# rho8 is sigma_8.
#
# sigma_8 = potential density - 1000
#
# Therefore:
#
# potential density = 1000 + sigma_8

absolute_density = 1000.0 + sigma8


# ------------------------------------------------------------
# Create clean CTD dataframe
# ------------------------------------------------------------

ctd_dataframe = pd.DataFrame({

    "depth_m":
        depth_positive,

    "salinity_PSU":
        salinity,

    "potential_temperature_C":
        potential_temperature,

    "sigma8_kg_m3":
        sigma8,

    "potential_density_800dbar_kg_m3":
        absolute_density

})


# ------------------------------------------------------------
# Save CTD CSV
# ------------------------------------------------------------

ctd_csv = os.path.join(
    CTD_FOLDER,
    "Challenger_Deep_Full_Depth_CTD.csv"
)

ctd_dataframe.to_csv(
    ctd_csv,
    index=False
)


# ------------------------------------------------------------
# Save CTD MATLAB file
# ------------------------------------------------------------

ctd_mat = os.path.join(
    CTD_FOLDER,
    "Challenger_Deep_Full_Depth_CTD.mat"
)

savemat(
    ctd_mat,
    {
        "depth_m": depth_positive,
        "salinity_PSU": salinity,
        "potential_temperature_C":
            potential_temperature,
        "sigma8_kg_m3": sigma8,
        "potential_density_800dbar_kg_m3":
            absolute_density
    },
    do_compression=True
)


print("\nCTD data saved.")

print(
    f"Number of observations: "
    f"{len(ctd_dataframe):,}"
)

print(
    f"Minimum depth: "
    f"{depth_positive.min():.2f} m"
)

print(
    f"Maximum depth: "
    f"{depth_positive.max():.2f} m"
)


# ============================================================
# 2. BATHYMETRY
# ============================================================

print("\n" + "=" * 60)
print("2. BATHYMETRY AND VERTICAL GRID")
print("=" * 60)


bathy_path = os.path.join(
    TEMP_FOLDER,
    BATHY_FILE
)

bathy = read_matlab_v73(
    bathy_path
)


print("\nBathymetry variables:")

for key, value in bathy.items():

    print(
        f"  {key}: "
        f"{np.asarray(value).shape}"
    )


# ------------------------------------------------------------
# Save complete MATLAB file
# ------------------------------------------------------------

bathy_mat = os.path.join(
    BATHY_FOLDER,
    "Bathymetry_and_Vertical_Grid.mat"
)

savemat(
    bathy_mat,
    bathy,
    do_compression=True
)


# ------------------------------------------------------------
# Save every numeric variable as CSV
# ------------------------------------------------------------

for key, value in bathy.items():

    save_csv(
        key,
        value,
        BATHY_FOLDER
    )


print("\nBathymetry saved.")


# ============================================================
# FUNCTION FOR MODEL DATA
# ============================================================

def process_model_file(
    source_file,
    output_folder,
    output_name
):

    print("\n" + "=" * 60)

    print(
        "MODEL DATA:",
        output_name
    )

    print("=" * 60)


    data = read_matlab_v73(
        source_file
    )


    print("\nVariables:")

    for key, value in data.items():

        print(
            f"  {key}: "
            f"{np.asarray(value).shape}"
        )


    # --------------------------------------------------------
    # Add absolute density
    # --------------------------------------------------------

    if "pden" in data:

        print(
            "\nAdding absolute potential density..."
        )

        data[
            "pden_absolute_kg_m3"
        ] = (
            data["pden"] + 1000.0
        )


    # --------------------------------------------------------
    # Save MATLAB
    # --------------------------------------------------------

    mat_filename = os.path.join(
        output_folder,
        output_name + ".mat"
    )

    savemat(
        mat_filename,
        data,
        do_compression=True
    )


    # --------------------------------------------------------
    # Save CSV files
    # --------------------------------------------------------

    for key, value in data.items():

        save_csv(
            key,
            value,
            output_folder
        )


    # --------------------------------------------------------
    # README
    # --------------------------------------------------------

    readme = os.path.join(
        output_folder,
        "README.txt"
    )

    with open(
        readme,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(
            output_name + "\n"
        )

        f.write(
            "\nVariables extracted:\n\n"
        )

        for key, value in data.items():

            f.write(
                f"{key}: "
                f"shape={np.asarray(value).shape}\n"
            )

        f.write(
            "\nDensity:\n"
        )

        f.write(
            "pden is sigma_0 (potential-density "
            "anomaly referenced to 0 dbar).\n"
        )

        f.write(
            "pden_absolute_kg_m3 = 1000 + pden.\n"
        )


    print(
        "\nModel data saved to:",
        output_folder
    )


# ============================================================
# 3. FIGURE 6 MODEL
# ============================================================

fig6_path = os.path.join(
    TEMP_FOLDER,
    MODEL_FIG6_FILE
)


process_model_file(

    fig6_path,

    FIG6_FOLDER,

    "Figure6_Model_Temp_Sal_Density"

)


# ============================================================
# 4. FIGURE 7.1 MODEL
# ============================================================

fig7_path = os.path.join(
    TEMP_FOLDER,
    MODEL_FIG7_FILE
)


process_model_file(

    fig7_path,

    FIG7_FOLDER,

    "Figure7_1_Model_Temp_Sal_Density"

)


# ============================================================
# ROOT README
# ============================================================

root_readme = os.path.join(
    OUTPUT_FOLDER,
    "README.txt"
)


with open(
    root_readme,
    "w",
    encoding="utf-8"
) as f:

    f.write(
        "CHALLENGER DEEP EXTRACTED DATA\n"
    )

    f.write(
        "==============================\n\n"
    )

    f.write(
        "01_Full_Depth_CTD_Profile\n"
    )

    f.write(
        "-------------------------\n"
    )

    f.write(
        "Full-depth observational CTD data.\n"
    )

    f.write(
        "Depth reaches approximately 10,850 m.\n\n"
    )

    f.write(
        "Variables:\n"
    )

    f.write(
        "depth_m\n"
        "salinity_PSU\n"
        "potential_temperature_C\n"
        "sigma8_kg_m3\n"
        "potential_density_800dbar_kg_m3\n\n"
    )

    f.write(
        "02_Bathymetry_and_Vertical_Grid\n"
    )

    f.write(
        "--------------------------------\n"
    )

    f.write(
        "Bathymetry and model vertical grid.\n\n"
    )

    f.write(
        "03_Model_Temp_Sal_Density_Figure6\n"
    )

    f.write(
        "---------------------------------\n"
    )

    f.write(
        "Model temperature, salinity and density.\n"
    )

    f.write(
        "Includes pden_absolute_kg_m3.\n\n"
    )

    f.write(
        "04_Model_Temp_Sal_Density_Figure7_1\n"
    )

    f.write(
        "------------------------------------\n"
    )

    f.write(
        "Model temperature, salinity and density.\n"
    )

    f.write(
        "Includes pden_absolute_kg_m3.\n\n"
    )

    f.write(
        "Density note:\n"
    )

    f.write(
        "CTD rho8 is sigma_8, so absolute potential density\n"
    )

    f.write(
        "is calculated as 1000 + sigma_8.\n"
    )

    f.write(
        "Model pden is sigma_0, so absolute potential density\n"
    )

    f.write(
        "is calculated as 1000 + pden.\n"
    )


# ============================================================
# CLEAN TEMPORARY FILES
# ============================================================

shutil.rmtree(
    TEMP_FOLDER
)


# ============================================================
# FINISHED
# ============================================================

print("\n")
print("=" * 60)
print("DONE!")
print("=" * 60)

print(
    "\nAll extracted data are in:"
)

print(
    os.path.abspath(
        OUTPUT_FOLDER
    )
)

print("\nFolder structure:")

print("""
Challenger_Deep_Extracted_Data/
│
├── README.txt
│
├── 01_Full_Depth_CTD_Profile/
│   ├── Challenger_Deep_Full_Depth_CTD.csv
│   └── Challenger_Deep_Full_Depth_CTD.mat
│
├── 02_Bathymetry_and_Vertical_Grid/
│   ├── Bathymetry_and_Vertical_Grid.mat
│   ├── topog.csv
│   ├── xc.csv
│   ├── yc.csv
│   ├── zc.csv
│   └── zf.csv
│
├── 03_Model_Temp_Sal_Density_Figure6/
│   ├── Figure6_Model_Temp_Sal_Density.mat
│   ├── ptmp.csv
│   ├── salt.csv
│   ├── pden.csv
│   ├── pden_absolute_kg_m3.csv
│   └── ...
│
└── 04_Model_Temp_Sal_Density_Figure7_1/
    ├── Figure7_1_Model_Temp_Sal_Density.mat
    ├── ptmp.csv
    ├── salt.csv
    ├── pden.csv
    ├── pden_absolute_kg_m3.csv
    └── ...
""")
