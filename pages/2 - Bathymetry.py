import os
import re
import numpy as np
import streamlit as st
import plotly.graph_objects as go
from scipy.io import loadmat
from ui import inject_global_style, render_nav, render_footer

st.set_page_config(
    page_title="Bathymetry · The Ocean Descent",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_global_style()
render_nav("bathymetry")

# -----------------------------
# Theme
# -----------------------------
st.markdown(
    """
    <style>
    :root {
        --bg: #050b12;
        --panel: rgba(10, 22, 34, 0.82);
        --panel-2: rgba(12, 29, 44, 0.72);
        --line: rgba(104, 185, 220, 0.18);
        --text: #e9f7ff;
        --muted: #8faabb;
        --cyan: #54d9ff;
        --cyan-soft: #8ce8ff;
    }

    .stApp {
        background:
            radial-gradient(circle at 82% 8%, rgba(31, 123, 163, 0.12), transparent 32%),
            radial-gradient(circle at 14% 38%, rgba(12, 82, 125, 0.10), transparent 28%),
            linear-gradient(180deg, #07131d 0%, #040a11 58%, #02060b 100%);
        color: var(--text);
    }

    [data-testid="stSidebar"] { background: #070d14; }

    .page-kicker {
        color: var(--cyan);
        text-transform: uppercase;
        letter-spacing: 0.22em;
        font-size: 0.72rem;
        font-weight: 700;
        margin-bottom: 0.55rem;
    }

    .page-title {
        font-size: clamp(2.5rem, 5vw, 5.4rem);
        line-height: 0.94;
        letter-spacing: -0.045em;
        font-weight: 800;
        margin: 0;
        color: #f2fbff;
    }

    .page-title span { color: var(--cyan); }

    .lead {
        max-width: 820px;
        color: #b7cbd6;
        font-size: 1.05rem;
        line-height: 1.75;
        margin-top: 1.1rem;
    }

    .section-label {
        color: var(--cyan);
        text-transform: uppercase;
        letter-spacing: 0.18em;
        font-size: 0.7rem;
        font-weight: 700;
        margin: 2.3rem 0 0.45rem;
    }

    .section-title {
        font-size: 1.65rem;
        font-weight: 750;
        letter-spacing: -0.025em;
        margin-bottom: 0.45rem;
    }

    .panel {
        background: linear-gradient(145deg, rgba(13, 31, 45, 0.88), rgba(5, 14, 22, 0.78));
        border: 1px solid var(--line);
        border-radius: 18px;
        padding: 1.15rem 1.25rem;
        box-shadow: 0 18px 60px rgba(0,0,0,0.20);
    }

    .small-note {
        color: var(--muted);
        font-size: 0.82rem;
        line-height: 1.55;
    }

    .metric-label {
        color: #7893a2;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        font-size: 0.66rem;
        font-weight: 700;
    }

    .metric-value {
        color: #f1fbff;
        font-size: 1.65rem;
        font-weight: 750;
        margin-top: 0.2rem;
    }

    .metric-sub { color: #8ba6b5; font-size: 0.76rem; }

    [data-testid="stSlider"] [data-baseweb="slider"] [role="progressbar"] {
        background: #54d9ff !important;
        box-shadow: 0 0 8px rgba(84,217,255,0.18) !important;
    }
    [data-testid="stSlider"] [data-baseweb="slider"] [role="slider"] {
        background: #54d9ff !important;
        border-color: #54d9ff !important;
        box-shadow: 0 0 0 4px rgba(84,217,255,0.10) !important;
    }

    footer { visibility: hidden; }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# Data loading
# -----------------------------
DATA_PATH = os.path.join(
    "Challenger_Deep_Extracted_Data",
    "02_Bathymetry_and_Vertical_Grid",
    "Bathymetry_and_Vertical_Grid.mat",
)

if not os.path.exists(DATA_PATH):
    st.error(
        "Bathymetry data file was not found. Make sure the existing "
        "Challenger_Deep_Extracted_Data folder is in the same directory as app.py."
    )
    st.stop()


@st.cache_data(show_spinner=False)
def load_bathymetry(path):
    data = loadmat(path, squeeze_me=True)
    topog = np.asarray(data["topog"], dtype=float)
    lon_grid = np.asarray(data["xc"], dtype=float)
    lat_grid = np.asarray(data["yc"], dtype=float)
    zc = np.asarray(data["zc"], dtype=float)
    zf = np.asarray(data["zf"], dtype=float)
    return topog, lon_grid, lat_grid, zc, zf


topog, lon_grid, lat_grid, zc, zf = load_bathymetry(DATA_PATH)

# The supplied grid stores longitude along the first dimension and latitude
# along the second dimension, while Plotly expects z[row=latitude, col=longitude].
lon = lon_grid[:, 0]
lat = lat_grid[0, :]
depth = topog.T

# The dataset's bathymetry field is positive downward depth in metres.
valid = np.isfinite(depth)
min_depth = float(np.nanmin(depth[valid]))
max_depth = float(np.nanmax(depth[valid]))

max_idx = np.unravel_index(np.nanargmax(depth), depth.shape)
deep_lat = float(lat[max_idx[0]])
deep_lon = float(lon[max_idx[1]])
deep_depth = float(depth[max_idx])

# -----------------------------
# Header
# -----------------------------
st.markdown('<div class="page-kicker">Mariana Trench · Seafloor geometry</div>', unsafe_allow_html=True)
st.markdown('<h1 class="page-title">THE <span>SEAFLOOR</span></h1>', unsafe_allow_html=True)
st.markdown(
    '<p class="lead">Before the descent reaches Challenger Deep, there is another story to see: the shape of the seafloor itself. Explore the supplied bathymetry grid and see how the trench cuts into the western Pacific.</p>',
    unsafe_allow_html=True,
)

# -----------------------------
# Key numbers
# -----------------------------
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown('<div class="metric-label">Grid longitude</div><div class="metric-value">%.2f°–%.2f°</div><div class="metric-sub">E</div>' % (lon.min(), lon.max()), unsafe_allow_html=True)
with c2:
    st.markdown('<div class="metric-label">Grid latitude</div><div class="metric-value">%.2f°–%.2f°</div><div class="metric-sub">N</div>' % (lat.min(), lat.max()), unsafe_allow_html=True)
with c3:
    st.markdown('<div class="metric-label">Deepest grid cell</div><div class="metric-value">%s m</div><div class="metric-sub">supplied bathymetry grid</div>' % f"{deep_depth:,.0f}", unsafe_allow_html=True)
with c4:
    st.markdown('<div class="metric-label">Deepest-cell position</div><div class="metric-value">%.2f° N</div><div class="metric-sub">%.2f° E</div>' % (deep_lat, deep_lon), unsafe_allow_html=True)

# -----------------------------
# 2D bathymetry map
# -----------------------------
st.markdown('<div class="section-label">01 · Bathymetric map</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">A trench is a landscape, not a point.</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="small-note">This view uses the actual <b>topog</b> field from the supplied bathymetry/model-grid dataset. Darker tones indicate greater depth. Hover over the grid to inspect longitude, latitude, and depth.</div>',
    unsafe_allow_html=True,
)

bathymetry_scale = [
    [0.00, "#0b2635"],
    [0.18, "#0c3f59"],
    [0.38, "#0a5c78"],
    [0.58, "#087c96"],
    [0.76, "#18a7ba"],
    [0.90, "#6bd7df"],
    [1.00, "#d8fbff"],
]

fig_map = go.Figure(
    go.Heatmap(
        x=lon,
        y=lat,
        z=depth,
        colorscale=bathymetry_scale,
        colorbar=dict(
            title=dict(text="Depth (m)", font=dict(color="#b9d1dc")),
            tickfont=dict(color="#9db5c0"),
            thickness=14,
            len=0.82,
        ),
        hovertemplate="Longitude: %{x:.3f}°E<br>Latitude: %{y:.3f}°N<br>Depth: %{z:,.0f} m<extra></extra>",
        zmin=min_depth,
        zmax=max_depth,
    )
)
fig_map.add_trace(
    go.Scatter(
        x=[deep_lon],
        y=[deep_lat],
        mode="markers+text",
        marker=dict(size=11, color="#f3fdff", line=dict(width=2, color="#54d9ff")),
        text=["Deepest grid cell"],
        textposition="top center",
        textfont=dict(color="#dff9ff", size=12),
        hovertemplate="Deepest supplied grid cell<br>%{x:.3f}°E, %{y:.3f}°N<br>%{customdata:,.0f} m<extra></extra>",
        customdata=[deep_depth],
        showlegend=False,
    )
)
fig_map.update_layout(
    height=650,
    margin=dict(l=10, r=10, t=10, b=10),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#cfe3ec"),
    xaxis=dict(title="Longitude (°E)", gridcolor="rgba(120,190,215,0.10)", zeroline=False),
    yaxis=dict(title="Latitude (°N)", gridcolor="rgba(120,190,215,0.10)", zeroline=False),
)
fig_map.update_xaxes(showline=True, linecolor="rgba(120,190,215,0.18)")
fig_map.update_yaxes(showline=True, linecolor="rgba(120,190,215,0.18)")
st.plotly_chart(fig_map, width="stretch", config={"displaylogo": False, "scrollZoom": True})

# -----------------------------
# 3D view
# -----------------------------
st.markdown('<div class="section-label">02 · Three-dimensional terrain</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Rotate the trench and see the relief.</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="small-note">The vertical axis is displayed with controlled exaggeration so the trench structure remains visible on screen. The underlying elevations are unchanged.</div>',
    unsafe_allow_html=True,
)

# Downsample for a responsive 3D scene while retaining the shape of the real grid.
step_lon = max(1, len(lon) // 110)
step_lat = max(1, len(lat) // 80)
lon_3d = lon[::step_lon]
lat_3d = lat[::step_lat]
depth_3d = depth[::step_lat, ::step_lon]

# Use the bathymetry depth itself as the 3D z value. This keeps the hover
# value tied directly to the plotted surface and avoids Surface customdata
# alignment issues in Plotly for rectangular grids. The z-axis is reversed
# so larger positive depths appear farther down.
fig_3d = go.Figure(
    go.Surface(
        x=lon_3d,
        y=lat_3d,
        z=depth_3d,
        colorscale=bathymetry_scale,
        showscale=False,
        hovertemplate="Longitude: %{x:.3f}°E<br>Latitude: %{y:.3f}°N<br>Depth: %{z:,.0f} m<extra></extra>",
        contours=dict(
            z=dict(show=True, usecolormap=False, highlight=False, project_z=False)
        ),
    )
)
fig_3d.add_trace(
    go.Scatter3d(
        x=[deep_lon],
        y=[deep_lat],
        z=[deep_depth],
        mode="markers+text",
        marker=dict(size=5, color="#f5fdff", line=dict(width=2, color="#54d9ff")),
        text=["Deepest grid cell"],
        textposition="top center",
        textfont=dict(color="#dff9ff", size=11),
        hovertemplate="Deepest supplied grid cell<br>%{x:.3f}°E, %{y:.3f}°N<br>Depth: %{z:,.0f} m<extra></extra>",
        showlegend=False,
    )
)
fig_3d.update_layout(
    height=700,
    margin=dict(l=0, r=0, t=0, b=0),
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#cfe3ec"),
    scene=dict(
        bgcolor="rgba(0,0,0,0)",
        xaxis=dict(title="Longitude", gridcolor="rgba(120,190,215,0.10)", zeroline=False),
        yaxis=dict(title="Latitude", gridcolor="rgba(120,190,215,0.10)", zeroline=False),
        zaxis=dict(title="Depth (m)", gridcolor="rgba(120,190,215,0.10)", zeroline=False, autorange="reversed"),
        aspectmode="manual",
        aspectratio=dict(x=1.35, y=0.95, z=0.48),
        camera=dict(eye=dict(x=1.55, y=1.45, z=1.0)),
    ),
)
st.plotly_chart(fig_3d, width="stretch", config={"displaylogo": False})

# -----------------------------
# Cross-section
# -----------------------------
st.markdown('<div class="section-label">03 · Transect</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Slice through the trench.</div>', unsafe_allow_html=True)

# Use the actual latitude values in the control rather than the array index.
lat_step = float(np.nanmedian(np.diff(lat))) if len(lat) > 1 else 0.01
selected_lat = st.slider(
    "Choose a latitude through the bathymetry grid",
    min_value=float(lat.min()),
    max_value=float(lat.max()),
    value=float(lat[max_idx[0]]),
    step=lat_step,
    format="%.2f° N",
    key="bathy_latitude",
)
lat_idx = int(np.nanargmin(np.abs(lat - selected_lat)))
selected_lat = float(lat[lat_idx])
section_depth = depth[lat_idx, :]

fig_section = go.Figure()
fig_section.add_trace(
    go.Scatter(
        x=lon,
        y=-section_depth,
        mode="lines",
        line=dict(color="#54d9ff", width=2.5),
        fill="tozeroy",
        fillcolor="rgba(84,217,255,0.12)",
        hovertemplate="Longitude: %{x:.3f}°E<br>Depth: %{customdata:,.0f} m<extra></extra>",
        customdata=section_depth,
        showlegend=False,
    )
)
section_max_idx = int(np.nanargmax(section_depth))
fig_section.add_trace(
    go.Scatter(
        x=[lon[section_max_idx]],
        y=[-section_depth[section_max_idx]],
        mode="markers+text",
        marker=dict(size=9, color="#f5fdff", line=dict(width=2, color="#54d9ff")),
        text=["deepest point on transect"],
        textposition="top center",
        textfont=dict(color="#dff9ff", size=11),
        showlegend=False,
    )
)
fig_section.update_layout(
    height=430,
    margin=dict(l=20, r=20, t=15, b=20),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#cfe3ec"),
    xaxis=dict(title="Longitude (°E)", gridcolor="rgba(120,190,215,0.10)"),
    yaxis=dict(title="Depth (m)", gridcolor="rgba(120,190,215,0.10)"),
)
st.plotly_chart(fig_section, width="stretch", config={"displaylogo": False})

# -----------------------------
# Provenance
# -----------------------------
st.markdown('<div class="section-label">04 · Data note</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">What you are looking at</div>', unsafe_allow_html=True)
st.markdown(
    """
    <div class="panel">
      <div class="small-note">
        <b>Dataset:</b> Bathymetry and vertical-grid data supplied with the Challenger Deep project extraction,
        represented by <b>Bathymetry_and_Vertical_Grid.mat</b> and the associated <b>topog</b>, <b>xc</b>, and <b>yc</b> fields.
        The grid covers approximately 138–149°E and 9–16°N. The page reports the deepest cell in this supplied grid;
        it should not be interpreted as a new measurement of the deepest point on Earth.
        <br><br>
        <b>Source:</b> Jiang, H. (2024), <i>Three-layer circulation in the world deepest trench</i>,
        Nature Communications dataset, Zenodo DOI 10.5281/zenodo.13870930.
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("---")
st.page_link(
    "pages/3 - Data & Methods.py",
    label="📘  Read the data & methods behind this map",
    width="stretch",
)
render_footer()
