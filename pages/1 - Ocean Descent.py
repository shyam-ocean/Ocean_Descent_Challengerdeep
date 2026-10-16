import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from scipy.io import loadmat

from depth_information import get_depth_information
from ui import inject_global_style, render_nav, render_footer


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="The Ocean Descent",
    page_icon="🌊",
    layout="wide"
)

inject_global_style()
render_nav("ocean")


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_ctd_data():

    file_path = (
        "Challenger_Deep_Extracted_Data/"
        "01_Full_Depth_CTD_Profile/"
        "Challenger_Deep_Full_Depth_CTD.mat"
    )

    mat = loadmat(file_path)

    depth = np.asarray(mat["depth_m"]).squeeze()
    salinity = np.asarray(mat["salinity_PSU"]).squeeze()
    temperature = np.asarray(mat["potential_temperature_C"]).squeeze()
    sigma8 = np.asarray(mat["sigma8_kg_m3"]).squeeze()
    potential_density = np.asarray(
        mat["potential_density_800dbar_kg_m3"]
    ).squeeze()

    df = pd.DataFrame({
        "depth_m": depth,
        "salinity_PSU": salinity,
        "potential_temperature_C": temperature,
        "sigma8_kg_m3": sigma8,
        "potential_density_800dbar_kg_m3": potential_density
    })

    df = df.replace(
        [np.inf, -np.inf],
        np.nan
    ).dropna()

    df = df.sort_values(
        "depth_m"
    ).reset_index(drop=True)

    return df


df = load_ctd_data()


# ============================================================
# PRESSURE ESTIMATION
# ============================================================

def estimate_pressure(depth_m):
    """
    Approximate hydrostatic pressure.

    This is NOT the measured CTD pressure.
    It is an educational approximation based on depth.

    Roughly:
        1 dbar ≈ 1 m of seawater
    """
    pressure_dbar = depth_m
    pressure_atm = pressure_dbar / 10.1325

    return pressure_dbar, pressure_atm


# ============================================================
# STAGE 1 VISUAL SYSTEM
# ============================================================

maximum_depth = float(df["depth_m"].max())


def depth_fraction(depth_m):
    return float(np.clip(depth_m / maximum_depth, 0.0, 1.0))


def ocean_palette(depth_m):
    """
    Return a depth-aware ocean palette.

    Scientific visual cue:
    - 0–200 m: sunlight still penetrates.
    - 200–1000 m: light falls rapidly through the twilight zone.
    - >1000 m: no sunlight reaches the water column, so the interface
      becomes very dark. This is a visual representation, not a measured
      light profile.
    """
    d = float(np.clip(depth_m, 0, maximum_depth))

    # Surface -> 200 m: blue ocean, with a gentle decrease in brightness.
    if d <= 200:
        t = d / 200.0
        c1 = np.array([8, 92, 132], dtype=float)
        c2 = np.array([4, 58, 94], dtype=float)

    # 200 -> 1000 m: rapid transition through the twilight zone.
    elif d <= 1000:
        t = (d - 200) / 800.0
        c1 = np.array([4, 58, 94], dtype=float)
        c2 = np.array([1, 13, 27], dtype=float)

    # Below 1000 m: aphotic zone. Keep a tiny navy component so the UI
    # remains visually navigable rather than becoming literal black.
    else:
        t = min((d - 1000) / 3000.0, 1.0)
        c1 = np.array([1, 13, 27], dtype=float)
        c2 = np.array([0, 5, 14], dtype=float)

    rgb = tuple(np.rint(c1 + (c2 - c1) * t).astype(int))

    # Accent stays oceanic/cyan. There is deliberately NO red surface marker.
    if d <= 1000:
        t2 = d / 1000.0
        a1 = np.array([54, 190, 225], dtype=float)
        a2 = np.array([35, 135, 190], dtype=float)
    else:
        t2 = min((d - 1000) / 5000.0, 1.0)
        a1 = np.array([35, 135, 190], dtype=float)
        a2 = np.array([120, 235, 255], dtype=float)

    accent = tuple(np.rint(a1 + (a2 - a1) * t2).astype(int))

    return rgb, accent


def rgb_string(rgb):
    """Convert an RGB tuple/list to a CSS rgb(...) string."""
    r, g, b = [int(v) for v in rgb]
    return f"rgb({r}, {g}, {b})"


def hex_string(rgb):
    """Convert an RGB tuple/list to a CSS hex string."""
    r, g, b = [int(np.clip(v, 0, 255)) for v in rgb]
    return f"#{r:02x}{g:02x}{b:02x}"


def render_depth_atmosphere(depth_m):
    """
    Presentation-only layer.

    Natural sunlight is treated as absent below ~1000 m. The floating
    lights represent decorative bioluminescence, not measured organisms.
    """
    bg_rgb, accent_rgb = ocean_palette(depth_m)
    bg = rgb_string(bg_rgb)
    accent = hex_string(accent_rgb)

    # Bioluminescence becomes a visual feature only in the aphotic ocean.
    # It grows from subtle at 1000 m to clearly visible in the hadal zone.
    bio_strength = np.clip((depth_m - 1000) / 4500, 0.0, 1.0)

    particles = [
        (7, 18, 5, 0.0),
        (14, 74, 7, 1.3),
        (23, 31, 4, 2.7),
        (30, 85, 6, 0.8),
        (39, 15, 5, 3.4),
        (51, 76, 8, 1.6),
        (63, 23, 5, 4.0),
        (72, 88, 6, 2.1),
        (82, 34, 8, 0.5),
        (92, 67, 5, 3.0),
        (95, 17, 4, 4.5),
        (4, 52, 6, 2.4),
    ]

    particle_html = ""
    for left, top, size, delay in particles:
        particle_html += (
            f'<span class="ocean-particle" '
            f'style="left:{left}vw;top:{top}vh;'
            f'width:{size}px;height:{size}px;'
            f'animation-delay:{delay}s;"></span>'
        )

    # At the surface these are invisible; below 1000 m they slowly appear.
    opacity = 0.0 + 0.58 * bio_strength

    st.html(
        f"""
        <style>
        :root {{
            --ocean-bg: {bg};
            --ocean-accent: {accent};
            --bio-opacity: {opacity:.3f};
        }}

        .stApp {{
            background:
                radial-gradient(
                    circle at 50% 0%,
                    rgba(55, 170, 210, {0.10 if depth_m < 1000 else 0.025:.3f}) 0%,
                    transparent 38%
                ),
                linear-gradient(
                    180deg,
                    rgba(0, 0, 0, 0.03) 0%,
                    rgba(0, 0, 0, 0.16) 100%
                ),
                var(--ocean-bg) !important;
            transition: background 0.8s ease;
        }}

        .main .block-container {{
            padding-top: 2.4rem;
            padding-bottom: 3rem;
            max-width: 1450px;
        }}

        [data-testid="stHeader"] {{
            background: transparent !important;
        }}

        [data-testid="stMetric"] {{
            background: rgba(2, 15, 30, 0.44);
            border: 1px solid rgba(150, 220, 240, 0.12);
            border-radius: 14px;
            padding: 12px 14px;
            backdrop-filter: blur(8px);
        }}

        /* Dynamic slider thumb: ocean/cyan throughout, never red. */
        [data-testid="stSlider"] [role="slider"],
        [data-testid="stSlider"] [data-baseweb="slider"] [role="slider"] {{
            background: {accent} !important;
            background-color: {accent} !important;
            border: 3px solid rgba(240,252,255,0.96) !important;
            box-shadow:
                0 0 0 3px rgba(130,230,255,0.08),
                0 0 20px {accent} !important;
            transition: background 0.5s ease, box-shadow 0.5s ease;
        }}

        [data-testid="stSlider"] [data-testid="stThumbValue"],
        [data-testid="stSlider"] [data-baseweb="slider"] [data-testid="stThumbValue"] {{
            color: {accent} !important;
        }}

        [data-testid="stSlider"] [data-baseweb="slider"] > div > div {{
            background: linear-gradient(
                90deg,
                #2fa9d1 0%,
                #167da7 22%,
                #0b4568 45%,
                #061b31 72%,
                #020b18 100%
            ) !important;
        }}

        /* Streamlit/BaseWeb paints the selected portion separately.
           Override that native progress segment so the default red never appears. */
        [data-testid="stSlider"] [data-baseweb="slider"] [role="progressbar"] {{
            background: {accent} !important;
            box-shadow: 0 0 8px rgba(60,205,255,0.18) !important;
        }}

        [data-testid="stSlider"] [data-baseweb="slider"] [data-testid="stTickBar"] > div {{
            background: transparent !important;
        }}

        [data-testid="stSlider"] {{
            padding-top: 8px;
            padding-bottom: 12px;
        }}

        /* Larger, brighter bioluminescent points. */
        .ocean-particle {{
            position: fixed;
            z-index: 1;
            border-radius: 50%;
            background: #d9fbff;
            opacity: var(--bio-opacity);
            box-shadow:
                0 0 8px rgba(220,252,255,1),
                0 0 22px rgba(80,225,255,0.95),
                0 0 42px rgba(60,205,255,0.50);
            animation: ocean-drift 8s ease-in-out infinite;
            pointer-events: none;
            transition: opacity 0.8s ease;
        }}

        @keyframes ocean-drift {{
            0%, 100% {{
                transform: translate3d(0, 8px, 0) scale(0.82);
                filter: brightness(0.75);
            }}
            50% {{
                transform: translate3d(16px, -26px, 0) scale(1.18);
                filter: brightness(1.45);
            }}
        }}

        .ocean-depth-badge {{
            display: inline-flex;
            align-items: center;
            gap: 9px;
            padding: 8px 13px;
            border-radius: 999px;
            border: 1px solid rgba(190,240,255,0.20);
            background: rgba(0, 10, 22, 0.46);
            color: rgba(235,250,255,0.92);
            font-size: 0.82rem;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            backdrop-filter: blur(8px);
        }}

        .ocean-dot {{
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: {accent};
            box-shadow: 0 0 14px {accent};
        }}

        .profile-note {{
            color: rgba(220,240,248,0.68);
            font-size: 0.86rem;
            margin-top: -5px;
        }}

        [data-testid="stPlotlyChart"] {{
            position: relative;
            z-index: 2;
        }}
        </style>

        {particle_html}
        """
    )


def make_profile_figure(
    x,
    y,
    selected_x,
    selected_y,
    title,
    x_title,
    line_color,
    accent,
    height=590,
    hero=False,
):
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=x,
            y=y,
            mode="lines",
            name="Observed profile",
            line=dict(
                color=line_color,
                width=3 if hero else 2.2,
            ),
            hovertemplate=(
                f"{x_title}: %{{x:.3f}}"
                "<br>Depth: %{y:,.0f} m"
                "<extra>Observed profile</extra>"
            ),
        )
    )

    # Current-depth guide.
    fig.add_hline(
        y=selected_y,
        line_width=1.5,
        line_dash="dot",
        line_color="rgba(210,245,255,0.70)",
    )

    # Large highlighted current point.
    fig.add_trace(
        go.Scatter(
            x=[selected_x],
            y=[selected_y],
            mode="markers",
            name="Selected depth",
            marker=dict(
                size=17 if hero else 14,
                color=accent,
                line=dict(
                    color="white",
                    width=2,
                ),
                opacity=1,
            ),
            hovertemplate=(
                f"{x_title}: %{{x:.3f}}"
                "<br>Depth: %{y:,.0f} m"
                "<extra>Selected depth</extra>"
            ),
        )
    )

    fig.update_layout(
        height=height,
        margin=dict(l=72, r=28, t=48, b=62),
        title=dict(
            text=title,
            x=0.02,
            xanchor="left",
            font=dict(size=20),
        ),
        xaxis=dict(
            title=x_title,
            gridcolor="rgba(160,215,235,0.13)",
            zerolinecolor="rgba(160,215,235,0.18)",
            tickfont=dict(size=12),
            title_font=dict(size=13),
        ),
        yaxis=dict(
            title="Depth (m)",
            autorange="reversed",
            gridcolor="rgba(160,215,235,0.13)",
            zerolinecolor="rgba(160,215,235,0.18)",
            tickfont=dict(size=12),
            title_font=dict(size=13),
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(1,15,29,0.35)",
        font=dict(
            color="rgba(235,248,255,0.90)",
            family="Arial, sans-serif",
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.01,
            xanchor="right",
            x=1,
            bgcolor="rgba(0,0,0,0)",
        ),
        hovermode="closest",
    )

    return fig


# ============================================================
# DEPTH SLIDER
# ============================================================

# Start at the surface with a natural ocean/cyan accent.
selected_depth = st.slider(
    "⬇️  Descend through the ocean",
    min_value=0,
    max_value=int(np.ceil(maximum_depth)),
    value=0,
    step=10,
    key="depth_slider",
)

render_depth_atmosphere(selected_depth)

bg_rgb, accent_rgb = ocean_palette(selected_depth)
accent = hex_string(accent_rgb)

# The slider itself is Streamlit's native widget. The colour bar below it
# makes the depth progression explicit and visually understandable.
st.markdown(
    f"""
    <div style="
        height:5px;
        width:100%;
        border-radius:999px;
        margin-top:-10px;
        margin-bottom:12px;
        background:linear-gradient(
            90deg,
            #2fa9d1 0%,
            #1593bd 25%,
            #07547d 52%,
            #071c35 78%,
            #9defff 100%
        );
        box-shadow:0 0 12px rgba(90,210,240,0.15);
    "></div>

    <div class="ocean-depth-badge">
        <span class="ocean-dot"></span>
        {selected_depth:,.0f} m below the surface
    </div>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# FIND NEAREST MEASURED POINT
# ============================================================

index = np.abs(
    df["depth_m"] - selected_depth
).argmin()

point = df.iloc[index]

actual_depth = float(point["depth_m"])
salinity = float(point["salinity_PSU"])
temperature = float(point["potential_temperature_C"])
sigma8 = float(point["sigma8_kg_m3"])
potential_density = float(
    point["potential_density_800dbar_kg_m3"]
)

pressure_dbar, pressure_atm = estimate_pressure(actual_depth)

zone = get_depth_information(actual_depth)


# ============================================================
# CURRENT LOCATION
# ============================================================

st.markdown("---")

import html
import re

safe_zone_name = html.escape(str(zone["name"]))

raw_description = str(zone["short_description"])
clean_description = re.sub(r"<[^>]*>", "", raw_description)
clean_description = html.unescape(clean_description).strip()
safe_description = html.escape(clean_description)

st.markdown(
    f"""
    <div style="
        padding: 8px 0 3px 0;
        position:relative;
        z-index:2;
    ">
        <div style="
            color:{accent};
            text-transform:uppercase;
            letter-spacing:0.14em;
            font-size:0.78rem;
            font-weight:700;
            margin-bottom:7px;
        ">
            CURRENT DEPTH ZONE
        </div>
        <h1 style="
            margin:0;
            color:rgba(245,252,255,0.96);
            font-size:2.35rem;
            line-height:1.08;
        ">
            {safe_zone_name}
        </h1>
        <p style="
            color:rgba(220,240,248,0.76);
            font-size:1.03rem;
            max-width:900px;
            margin-top:10px;
        ">
            <strong>{actual_depth:,.0f} m</strong> below the ocean surface
            · {safe_description}
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# DASHBOARD
# ============================================================

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Depth",
    f"{actual_depth:,.0f} m"
)

col2.metric(
    "Salinity",
    f"{salinity:.3f} PSU"
)

col3.metric(
    "Potential temperature",
    f"{temperature:.3f} °C"
)

col4.metric(
    "Estimated pressure",
    f"{pressure_atm:,.0f} atm"
)


# ============================================================
# SECONDARY DENSITY INFORMATION
# ============================================================

st.markdown(
    f"""
    <div style="
        text-align:center;
        color:rgba(220,240,248,0.70);
        font-size:0.90rem;
        margin:8px 0 18px 0;
        position:relative;
        z-index:2;
    ">
        Potential density: <strong>{potential_density:.3f} kg/m³</strong>
        &nbsp;·&nbsp;
        σ₈: <strong>{sigma8:.3f} kg/m³</strong>
        &nbsp;·&nbsp;
        Estimated pressure: <strong>{pressure_dbar:,.0f} dbar</strong>
    </div>
    """,
    unsafe_allow_html=True,
)

st.caption(
    "Pressure is estimated from depth for visualization. "
    "It is not a raw pressure measurement from this profile. "
    "Density is potential density referenced to 800 dbar."
)


# ============================================================
# PROFILE: SALINITY
# ============================================================

st.markdown("---")

st.header("📈 Salinity profile")
st.markdown(
    '<div class="profile-note">The bright marker shows the measurement nearest to your selected depth.</div>',
    unsafe_allow_html=True,
)

fig_salinity = make_profile_figure(
    df["salinity_PSU"],
    df["depth_m"],
    salinity,
    actual_depth,
    "Salinity through the water column",
    "Salinity (PSU)",
    "#4cc9f0",
    accent,
    height=600,
    hero=True,
)

st.plotly_chart(
    fig_salinity,
    width="stretch",
    config={"displaylogo": False, "responsive": True},
)


# ============================================================
# PROFILE: TEMPERATURE
# ============================================================

st.markdown("---")

st.header("🌡️ Potential temperature profile")

fig_temperature = make_profile_figure(
    df["potential_temperature_C"],
    df["depth_m"],
    temperature,
    actual_depth,
    "Potential temperature through the water column",
    "Potential temperature (°C)",
    "#f4a261",
    accent,
    height=560,
)

st.plotly_chart(
    fig_temperature,
    width="stretch",
    config={"displaylogo": False, "responsive": True},
)


# ============================================================
# PROFILE: DENSITY
# ============================================================

st.markdown("---")

st.header("⚖️ Potential density profile")

fig_density = make_profile_figure(
    df["potential_density_800dbar_kg_m3"],
    df["depth_m"],
    potential_density,
    actual_depth,
    "Potential density through the water column",
    "Potential density referenced to 800 dbar (kg/m³)",
    "#8ecae6",
    accent,
    height=560,
)

st.plotly_chart(
    fig_density,
    width="stretch",
    config={"displaylogo": False, "responsive": True},
)


# ============================================================
# SCIENTIFIC INFORMATION
# ============================================================

st.markdown("---")

st.header("🔬 What is happening here?")

with st.expander("🌊 Physical environment", expanded=True):
    st.write(zone["physical"])

with st.expander("🧪 Chemistry"):
    st.write(zone["chemistry"])

with st.expander("🦠 Life"):
    st.write(zone["life"])

with st.expander("🪨 Geology & sediments"):
    st.write(zone["geology"])

with st.expander("📡 How was it measured?"):
    st.write(zone["measurement"])


# ============================================================
# INTERESTING FACTS
# ============================================================

st.markdown("---")

st.header("💡 Interesting facts")

for fact in zone["facts"]:
    st.markdown(f"• {fact}")


# ============================================================
# DATA SOURCE
# ============================================================

st.markdown("---")

st.header("📚 Data & references")

st.markdown(
    """
    **Primary dataset**

    Jiang, H. (2024). *Three-layer circulation in the world deepest
    trench* [Dataset]. Zenodo.

    DOI: **10.5281/zenodo.13870930**
    """
)

st.markdown(
    """
    **Profile used**

    The visualization uses the CTD profile contained in the source
    data associated with the study. The profile reaches approximately
    **10,850 m**.
    """
)

st.markdown(
    """
    **Important scientific note**

    Salinity and potential temperature are taken directly from the
    supplied profile.

    The density variable in the dataset is **σ₈**, a potential-density
    anomaly referenced to 800 dbar. The value displayed as potential
    density is obtained by adding 1000 kg/m³ to σ₈.

    Pressure in this first version is an **estimated hydrostatic
    pressure derived from depth**, not a raw pressure measurement.
    """
)


# ============================================================
# STAGE 4 NAVIGATION
# ============================================================

st.markdown("---")
st.page_link(
    "pages/3 - Data & Methods.py",
    label="📘  Read the data & methods behind this descent",
    width="stretch",
)

render_footer()
