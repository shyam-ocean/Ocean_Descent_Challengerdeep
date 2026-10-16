import streamlit as st


PRIMARY = "#54d9ff"
BG = "#02080f"
PANEL = "#07131d"
TEXT = "#eaf7fb"
MUTED = "#8fa8b5"


def inject_global_style():
    st.html(
        """
        <style>
        :root {
            --od-cyan: #54d9ff;
            --od-cyan-soft: #9defff;
            --od-bg: #02080f;
            --od-panel: #07131d;
            --od-text: #eaf7fb;
            --od-muted: #8fa8b5;
        }

        [data-testid="stSidebar"] {
            display: none !important;
        }

        [data-testid="stHeader"] {
            background: rgba(0,0,0,0) !important;
        }

        .od-nav {
            max-width: 1380px;
            margin: 0 auto 22px auto;
            padding: 10px 0 12px 0;
            border-bottom: 1px solid rgba(120, 205, 230, 0.12);
        }

        .od-brand {
            color: #f1fbff;
            font-size: 0.82rem;
            font-weight: 800;
            letter-spacing: 0.16em;
            text-transform: uppercase;
            padding-top: 7px;
            white-space: nowrap;
        }

        .od-brand span {
            color: var(--od-cyan);
        }

        .od-nav a,
        [data-testid="stPageLink"] a {
            color: rgba(220, 241, 247, 0.68) !important;
            text-decoration: none !important;
            font-size: 0.82rem !important;
            font-weight: 650 !important;
            letter-spacing: 0.04em;
            border: 1px solid transparent !important;
            border-radius: 999px !important;
            padding: 7px 13px !important;
            transition: all 0.18s ease;
        }

        .od-nav a:hover,
        [data-testid="stPageLink"] a:hover {
            color: #f2fcff !important;
            background: rgba(84, 217, 255, 0.08) !important;
            border-color: rgba(84, 217, 255, 0.18) !important;
        }

        .od-nav-active {
            display: inline-block;
            color: #f4fdff;
            background: rgba(84, 217, 255, 0.10);
            border: 1px solid rgba(84, 217, 255, 0.22);
            border-radius: 999px;
            padding: 7px 13px;
            font-size: 0.82rem;
            font-weight: 700;
            letter-spacing: 0.04em;
        }

        .od-section-rule {
            height: 1px;
            background: linear-gradient(90deg, rgba(84,217,255,0.25), rgba(84,217,255,0.04), transparent);
            margin: 38px 0 24px 0;
        }

        .od-footer {
            margin-top: 54px;
            padding: 22px 0 34px 0;
            border-top: 1px solid rgba(120, 205, 230, 0.10);
            color: rgba(143,168,181,0.62);
            font-size: 0.72rem;
            line-height: 1.7;
        }

        .od-footer strong { color: rgba(221,242,248,0.78); }

        @media (max-width: 900px) {
            .od-nav { margin-bottom: 12px; }
            .od-brand { font-size: 0.70rem; }
            .od-nav a, .od-nav-active { font-size: 0.74rem !important; padding: 6px 9px !important; }
        }
        </style>
        """
    )


def render_nav(active: str):
    labels = {
        "home": "Home",
        "ocean": "Ocean Descent",
        "bathymetry": "Bathymetry",
        "methods": "Data & Methods",
    }

    st.markdown('<div class="od-nav">', unsafe_allow_html=True)
    cols = st.columns([2.2, 0.8, 1.15, 0.95, 1.15], gap="small")

    with cols[0]:
        st.markdown('<div class="od-brand">THE OCEAN <span>DESCENT</span></div>', unsafe_allow_html=True)

    destinations = [
        (1, "home", "app.py"),
        (2, "ocean", "pages/1 - Ocean Descent.py"),
        (3, "bathymetry", "pages/2 - Bathymetry.py"),
        (4, "methods", "pages/3 - Data & Methods.py"),
    ]

    for col_idx, key, path in destinations:
        with cols[col_idx]:
            if active == key:
                st.markdown(f'<div class="od-nav-active">{labels[key]}</div>', unsafe_allow_html=True)
            else:
                st.page_link(path, label=labels[key], width="stretch")

    st.markdown('</div>', unsafe_allow_html=True)


def render_footer():
    st.markdown(
        """
        <div class="od-footer">
            <strong>THE OCEAN DESCENT</strong> · Interactive scientific visualization<br>
            Challenger Deep CTD and bathymetry data · Jiang (2024) · Zenodo DOI 10.5281/zenodo.13870930
        </div>
        """,
        unsafe_allow_html=True,
    )
