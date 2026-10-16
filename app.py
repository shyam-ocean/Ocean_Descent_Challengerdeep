import streamlit as st

from ui import inject_global_style, render_nav, render_footer

st.set_page_config(
    page_title="The Ocean Descent",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_global_style()
render_nav("home")


# ---------------------------------------------------------------------
# Landing-page styling
# ---------------------------------------------------------------------
st.html(
"""
<style>
    .stApp {
        background:
            radial-gradient(circle at 50% 12%, rgba(31, 122, 168, 0.24), transparent 34%),
            radial-gradient(circle at 15% 70%, rgba(9, 77, 109, 0.16), transparent 30%),
            linear-gradient(180deg, #03131d 0%, #020b12 48%, #01070c 100%);
        color: #eaf7fb;
    }

    [data-testid="stHeader"] {
        background: rgba(0, 0, 0, 0);
    }

    [data-testid="stSidebar"] {
        display: none;
    }

    .landing-wrap {
        max-width: 1180px;
        margin: 0 auto;
        padding: 52px 18px 70px 18px;
    }

    .eyebrow {
        display: inline-block;
        padding: 7px 13px;
        border: 1px solid rgba(102, 220, 245, 0.28);
        border-radius: 999px;
        color: #8bdff1;
        background: rgba(23, 116, 151, 0.10);
        font-size: 0.74rem;
        font-weight: 700;
        letter-spacing: 0.18em;
        text-transform: uppercase;
    }

    .hero {
        position: relative;
        min-height: 610px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        padding: 42px 0 70px 0;
        overflow: hidden;
    }

    .hero::before {
        content: "";
        position: absolute;
        width: 520px;
        height: 520px;
        right: -130px;
        top: 30px;
        border-radius: 50%;
        background: radial-gradient(
            circle,
            rgba(45, 194, 230, 0.12) 0%,
            rgba(45, 194, 230, 0.035) 35%,
            transparent 70%
        );
        filter: blur(2px);
        pointer-events: none;
    }

    .hero::after {
        content: "";
        position: absolute;
        left: -10%;
        right: -10%;
        bottom: 0;
        height: 150px;
        background:
            linear-gradient(180deg, transparent, rgba(0, 5, 9, 0.88)),
            radial-gradient(
                ellipse at 50% 100%,
                rgba(22, 73, 94, 0.38),
                transparent 62%
            );
        pointer-events: none;
    }

    .hero-kicker {
        color: #6fd9ef;
        font-size: 0.82rem;
        font-weight: 700;
        letter-spacing: 0.22em;
        text-transform: uppercase;
        margin-bottom: 18px;
    }

    .hero-title {
        max-width: 920px;
        margin: 0;
        font-size: clamp(3.4rem, 8vw, 7.4rem);
        line-height: 0.88;
        letter-spacing: -0.055em;
        font-weight: 800;
        color: #f2fbfd;
        text-shadow: 0 8px 45px rgba(0, 0, 0, 0.42);
    }

    .hero-title span {
        color: #6fdaef;
    }

    .hero-subtitle {
        max-width: 720px;
        margin-top: 30px;
        font-size: clamp(1.05rem, 1.8vw, 1.35rem);
        line-height: 1.65;
        color: rgba(226, 244, 248, 0.72);
    }

    .depth-line {
        margin-top: 34px;
        width: min(720px, 100%);
        height: 1px;
        background: linear-gradient(
            90deg,
            rgba(99, 220, 241, 0.55),
            rgba(99, 220, 241, 0.12),
            transparent
        );
    }

    .depth-caption {
        margin-top: 12px;
        color: rgba(167, 219, 231, 0.56);
        font-size: 0.78rem;
        letter-spacing: 0.11em;
        text-transform: uppercase;
    }

    .section {
        margin-top: 22px;
        padding: 34px 0;
    }

    .section-label {
        color: #63d5ed;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.20em;
        text-transform: uppercase;
        margin-bottom: 12px;
    }

    .section-title {
        color: #eefafd;
        font-size: clamp(1.8rem, 3vw, 2.7rem);
        line-height: 1.1;
        margin-bottom: 14px;
        font-weight: 750;
    }

    .section-copy {
        max-width: 850px;
        color: rgba(218, 239, 244, 0.70);
        font-size: 1rem;
        line-height: 1.8;
    }

    .story-card {
        min-height: 260px;
        padding: 28px;
        border: 1px solid rgba(105, 211, 239, 0.13);
        border-radius: 18px;
        background:
            linear-gradient(
                145deg,
                rgba(11, 42, 55, 0.48),
                rgba(3, 16, 24, 0.68)
            );
        box-shadow: 0 22px 70px rgba(0, 0, 0, 0.20);
    }

    .story-number {
        color: rgba(104, 218, 240, 0.48);
        font-size: 0.75rem;
        letter-spacing: 0.18em;
        font-weight: 700;
        text-transform: uppercase;
        margin-bottom: 24px;
    }

    .story-title {
        color: #eaf9fc;
        font-size: 1.25rem;
        font-weight: 700;
        margin-bottom: 12px;
    }

    .story-copy {
        color: rgba(211, 235, 240, 0.65);
        line-height: 1.7;
        font-size: 0.93rem;
    }

    .data-strip {
        margin-top: 28px;
        padding: 22px 24px;
        border-left: 2px solid rgba(91, 215, 238, 0.65);
        background: rgba(11, 54, 70, 0.20);
    }

    .data-strip strong {
        color: #eaf9fc;
    }

    .data-strip span {
        color: rgba(211, 235, 240, 0.62);
    }

    .footer {
        margin-top: 65px;
        padding-top: 24px;
        border-top: 1px solid rgba(105, 211, 239, 0.10);
        color: rgba(175, 215, 224, 0.45);
        font-size: 0.76rem;
        line-height: 1.7;
    }

    div[data-testid="stButton"] > button,
    div[data-testid="stPageLink"] > a {
        border-radius: 999px !important;
    }

    @media (max-width: 800px) {
        .landing-wrap {
            padding-top: 25px;
        }

        .hero {
            min-height: 520px;
        }

        .hero-title {
            font-size: clamp(3rem, 16vw, 5.2rem);
        }
    }
</style>
"""
)

st.html(
"""
<div class="landing-wrap">

    <div class="hero">
        <div class="eyebrow">Mariana Trench · Challenger Deep</div>
        <div class="hero-kicker">A scientific descent into the deep ocean</div>

        <h1 class="hero-title">
            THE OCEAN<br><span>DESCENT</span>
        </h1>

        <p class="hero-subtitle">
            What happens to the ocean as you travel from sunlight at the surface
            to the deepest known point on Earth?
            Explore a real CTD profile from the Challenger Deep and descend
            through more than ten kilometres of water.
        </p>

        <div class="depth-line"></div>
        <div class="depth-caption">
            Surface → Twilight → Midnight → Hadal
        </div>
    </div>

"""
)

nav1, nav2 = st.columns(2, gap="medium")
with nav1:
    st.page_link(
        "pages/1 - Ocean Descent.py",
        label="🌊  Begin the descent",
        width="stretch",
    )
with nav2:
    st.page_link(
        "pages/2 - Bathymetry.py",
        label="🗺️  Explore the seafloor",
        width="stretch",
    )

st.html(
"""
    <div class="section">
        <div class="section-label">01 · The question</div>
        <div class="section-title">It started with a simple search.</div>
        <div class="section-copy">
            One of the most frequently searched questions in Google about our
            planet is deceptively simple: <em>What is the deepest part of the ocean?</em>
            <br><br>
            The instant answer is Challenger Deep—nearly 11,000 meters down.
            But knowing a name or a number doesn’t tell you what actually
            happens along the way. As you descend, the ocean undergoes radical
            shifts: sunlight vanishes, crushing pressure builds, temperatures
            plummet, and salinity and density redefine the boundaries of life
            itself. This project translates real oceanographic data into an
            intuitive journey, breaking down the water column so anyone can see
            the hidden transitions that shape the abyss.
        </div>
    </div>
"""
)

c1, c2, c3 = st.columns(3, gap="large")

with c1:
    st.html(
"""
        <div class="story-card">
            <div class="story-number">02 · Descend</div>
            <div class="story-title">Follow the water column</div>
            <div class="story-copy">
                Move the depth control from the surface toward Challenger Deep
                and watch the environment change continuously rather than as a
                collection of disconnected facts.
            </div>
        </div>
"""
    )

with c2:
    st.html(
"""
        <div class="story-card">
            <div class="story-number">03 · Measure</div>
            <div class="story-title">Read the real observations</div>
            <div class="story-copy">
                The descent is driven by CTD measurements of salinity,
                potential temperature and potential density, paired with an
                estimated hydrostatic pressure for depth context.
            </div>
        </div>
"""
    )

with c3:
    st.html(
"""
        <div class="story-card">
            <div class="story-number">04 · Experience</div>
            <div class="story-title">See the ocean lose its light</div>
            <div class="story-copy">
                The visual environment becomes darker with depth. Below the
                sunlit ocean, the interface shifts toward the near-black
                conditions of the deep sea, with bioluminescent light emerging
                in the darkness.
            </div>
        </div>
"""
    )

st.html(
"""
    <div class="data-strip">
        <strong>The dataset:</strong>
        <span>
            a full-depth CTD profile reaching approximately 10,850 m in the
            Challenger Deep. The interactive page uses the cleaned profile
            already prepared for this project.
        </span>
    </div>
"""
)

st.html(
"""
    <div class="section">
        <div class="section-label">05 · Before you descend</div>
        <div class="section-title">There is no single “deep ocean.”</div>
        <div class="section-copy">
            The descent is a continuous transition through different physical
            environments. The visual design is intended to make that transition
            intuitive first, while the measurements and explanations provide
            the scientific detail underneath it.
        </div>
    </div>
"""
)

st.page_link(
    "pages/1 - Ocean Descent.py",
    label="Continue to the interactive CTD profile  →",
    width="stretch",
)

st.html(
"""
    <div class="footer">
        <strong>The Ocean Descent</strong><br>
        An interactive exploration of the Challenger Deep water column.<br>
        Stage 2 · Landing page
    </div>

</div>
"""
)


st.html("""
<div class="section">
  <div class="section-label">06 · Open the notebook</div>
  <div class="section-title">Want to know exactly how the journey is built?</div>
  <div class="section-copy">Read the data provenance, variables, pressure convention, bathymetry handling and visual assumptions behind the experience.</div>
</div>
""")

st.page_link("pages/3 - Data & Methods.py", label="📘  Read data & methods", width="stretch")

render_footer()
