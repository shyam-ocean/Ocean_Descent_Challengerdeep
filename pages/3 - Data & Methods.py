import streamlit as st

from ui import inject_global_style, render_nav, render_footer

st.set_page_config(
    page_title="Data & Methods · The Ocean Descent",
    page_icon="📘",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_global_style()
render_nav("methods")

st.html(
"""
<style>
.methods-wrap { max-width: 1180px; margin: 0 auto; }
.methods-kicker {
    color: #54d9ff; text-transform: uppercase; letter-spacing: .22em;
    font-size: .72rem; font-weight: 750; margin-bottom: .55rem;
}
.methods-title {
    margin: 0; color: #f1fbff; font-size: clamp(2.7rem, 6vw, 5.7rem);
    line-height: .92; letter-spacing: -.05em; font-weight: 800;
}
.methods-title span { color: #54d9ff; }
.methods-lead {
    max-width: 850px; color: #b7cbd6; font-size: 1.04rem;
    line-height: 1.8; margin: 1.15rem 0 2rem;
}
.method-card {
    height: 100%; padding: 24px; border-radius: 18px;
    border: 1px solid rgba(105,211,239,.14);
    background: linear-gradient(145deg, rgba(11,35,49,.72), rgba(4,13,21,.82));
    box-shadow: 0 18px 60px rgba(0,0,0,.18);
}
.method-number { color: rgba(84,217,255,.58); font-size: .70rem; font-weight: 750;
    letter-spacing: .18em; text-transform: uppercase; margin-bottom: 15px; }
.method-title { color: #effbff; font-size: 1.18rem; font-weight: 750; margin-bottom: 9px; }
.method-copy { color: rgba(211,235,240,.68); line-height: 1.72; font-size: .91rem; }
.method-copy b { color: #eaf9fc; }
.source-card { padding: 22px 24px; border-left: 2px solid rgba(84,217,255,.65);
    background: rgba(11,54,70,.18); margin-top: 20px; }
.source-card a { color: #7ce4fa; text-decoration: none; }
.source-card a:hover { text-decoration: underline; }
.section-kicker { color: #54d9ff; text-transform: uppercase; letter-spacing: .18em;
    font-size: .70rem; font-weight: 750; margin-top: 2.4rem; margin-bottom: .45rem; }
.section-title { color: #eefafd; font-size: 1.7rem; font-weight: 760; letter-spacing: -.025em; }
.table-like { width:100%; border-collapse:collapse; margin-top:14px; }
.table-like td { padding: 11px 12px; border-bottom:1px solid rgba(120,205,230,.09); color:rgba(211,235,240,.70); vertical-align:top; }
.table-like td:first-child { color:#eaf9fc; font-weight:700; width:32%; }
.note { color:rgba(175,215,224,.60); font-size:.80rem; line-height:1.65; }
</style>
<div class="methods-wrap">
  <div class="methods-kicker">Scientific provenance · assumptions · reproducibility</div>
  <h1 class="methods-title">DATA <span>& METHODS</span></h1>
  <p class="methods-lead">
    The Ocean Descent is a visual interpretation of supplied Challenger Deep
    observations and bathymetry. This page separates what comes directly from
    the dataset from what is an interface choice or an educational approximation.
  </p>
</div>
"""
)

st.markdown('<div class="section-kicker">01 · Primary source</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Jiang (2024) · Challenger Deep dataset</div>', unsafe_allow_html=True)
st.markdown(
    """
    <div class="source-card">
      <div class="method-copy">
        <b>Jiang, H. (2024).</b> <i>Three-layer circulation in the world deepest trench</i> [Dataset]. Zenodo.<br>
        DOI: <a href="https://doi.org/10.5281/zenodo.13870930" target="_blank">10.5281/zenodo.13870930</a>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="section-kicker">02 · CTD profile</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">What is plotted on the descent page?</div>', unsafe_allow_html=True)

c1, c2 = st.columns(2, gap="large")
with c1:
    st.markdown(
        """
        <div class="method-card">
          <div class="method-number">Profile variables</div>
          <div class="method-copy">
            The cleaned CTD profile uses the supplied <b>depth_m</b>,
            <b>salinity_PSU</b>, <b>potential_temperature_C</b>,
            <b>sigma8_kg_m3</b>, and <b>potential_density_800dbar_kg_m3</b>
            fields. Missing and non-finite values are removed and the profile
            is sorted by depth.
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with c2:
    st.markdown(
        """
        <div class="method-card">
          <div class="method-number">Selected-depth logic</div>
          <div class="method-copy">
            The depth control does <b>not interpolate</b> the observations.
            For each selected depth, the interface chooses the nearest measured
            CTD record and displays that record's salinity, temperature and density.
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown('<div class="section-kicker">03 · Pressure and density</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Two conventions are intentionally made explicit.</div>', unsafe_allow_html=True)
st.markdown(
    """
    <table class="table-like">
      <tr><td>Pressure</td><td>The displayed pressure is an <b>estimated hydrostatic pressure</b>, using the project convention 1 dbar ≈ 1 m of seawater: pressure_dbar = depth_m, then pressure_atm = pressure_dbar / 10.1325. It is not presented as a raw CTD pressure measurement.</td></tr>
      <tr><td>Potential density</td><td>The supplied <b>sigma8</b> field is a potential-density anomaly referenced to 800 dbar. The displayed potential-density value is the anomaly plus 1000 kg/m³.</td></tr>
    </table>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="section-kicker">04 · Bathymetry</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">The seafloor page uses the supplied model grid.</div>', unsafe_allow_html=True)

c1, c2 = st.columns(2, gap="large")
with c1:
    st.markdown(
        """
        <div class="method-card">
          <div class="method-number">Source fields</div>
          <div class="method-copy">
            The bathymetry page reads <b>topog</b>, <b>xc</b>, <b>yc</b>,
            <b>zc</b>, and <b>zf</b> from <b>Bathymetry_and_Vertical_Grid.mat</b>.
            The displayed horizontal grid spans approximately 138–149°E and 9–16°N.
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with c2:
    st.markdown(
        """
        <div class="method-card">
          <div class="method-number">Deepest cell</div>
          <div class="method-copy">
            The reported <b>10,767 m</b> value is the deepest cell in the supplied
            bathymetry grid, located at approximately <b>142.441°E, 11.356°N</b>.
            It is not claimed here as a new measurement of Earth's deepest point.
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown('<div class="section-kicker">05 · Plotting choices</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">What is scientific data, and what is visualization?</div>', unsafe_allow_html=True)
st.markdown(
    """
    <table class="table-like">
      <tr><td>2D bathymetry</td><td>Uses the supplied <b>topog</b> grid directly as depth, with longitude and latitude from the supplied coordinate grids.</td></tr>
      <tr><td>3D bathymetry</td><td>Uses the same depth field as the surface z-values. The rendered surface is downsampled only to keep the interactive scene responsive; the underlying data are unchanged.</td></tr>
      <tr><td>Vertical exaggeration</td><td>The 3D scene uses a controlled aspect ratio to make trench relief readable on screen. This changes appearance, not the underlying depth values.</td></tr>
      <tr><td>Light zones</td><td>The interface uses 0–200 m as the euphotic/sunlight zone, 200–1,000 m as the dysphotic/twilight zone, and below 1,000 m as aphotic. These boundaries are educational visual cues based on NOAA Ocean Exploration guidance.</td></tr>
      <tr><td>Bioluminescence</td><td>The glowing particles in the descent interface are an illustrative visual layer. They are not measurements of organism abundance or observed light intensity at the selected depth.</td></tr>
    </table>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="section-kicker">06 · External scientific reference</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Ocean light zones</div>', unsafe_allow_html=True)
st.markdown(
    """
    <div class="source-card">
      <div class="method-copy">
        NOAA Ocean Exploration describes the upper 200 m as the euphotic zone,
        200–1,000 m as the dysphotic or twilight zone, and depths below 1,000 m
        as aphotic, where sunlight does not penetrate.<br><br>
        <a href="https://oceanexplorer.noaa.gov/ocean-fact/light-distributed/" target="_blank">NOAA Ocean Exploration · How far does light travel in the ocean?</a>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="section-kicker">07 · Reproducibility note</div>', unsafe_allow_html=True)
st.markdown(
    """
    <div class="method-card">
      <div class="method-copy">
        The visualizations are generated from the local extracted MAT files
        included with this project. No bathymetry values are manually entered
        into the plots. The interactive controls change the view or select the
        nearest supplied observation; they do not alter the source measurements.
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("---")
st.page_link("app.py", label="← Back to the project", width="stretch")
render_footer()
