"""

This is the main page, that you have to run with "streamlit run" to launch the app locally.
Streamlit automatically create the tabs in the left sidebar from the .py files located in /pages
Here we just have the home page, with a short description of the tabs, and some images

"""


import streamlit as st

st.set_page_config(
    page_title="Home page",
    page_icon="👋",
    layout="centered")

# Subtle animated gradient background
st.markdown(
        """
        <style>
            @keyframes gradientShift {
                0% { background-position: 0% 50%; }
                50% { background-position: 100% 50%; }
                100% { background-position: 0% 50%; }
            }
            .stApp {
                background: linear-gradient(-45deg, rgba(14,165,233,0.08), rgba(34,197,94,0.08), rgba(244,63,94,0.08));
                background-size: 400% 400%;
                animation: gradientShift 18s ease infinite;
            }
            /* Card-style container */
            .hero-card {
                padding: 1.2rem 1.4rem;
                border-radius: 16px;
                background: rgba(255,255,255,0.65);
                box-shadow: 0 8px 28px rgba(0,0,0,0.08);
                backdrop-filter: blur(6px);
            }
            .caption { font-size: 0.85rem; color: #6b7280; }
        </style>
        """,
        unsafe_allow_html=True,
)

# Main Description
st.title("👋 LNP Formulation Calculator")
st.markdown("Designed for quick, accurate lipid nanoparticle (LNP) formulation workflows for pDNA and mRNA.")
st.markdown("Developed by **Yue Xu**, YongLi Lab @ BCM — more at https://yuexu95.github.io/")
st.markdown("Have feedback or feature requests? Email: **yue.xu@bcm.edu**.")

# Description of the features. 
with st.container():
    st.markdown("""
    ### Explore in the left sidebar

    - **General info**: Overview of LNP formulation concepts and calculation principles.
    - **pDNA Formulation**: Calculator for plasmid DNA, with N/P ratio and detailed volumes.
    - **mRNA Formulation**: Calculator for mRNA, mirroring the pDNA workflow and outputs.
    """)

    # Hero visuals
    colA, colB = st.columns([1, 1])
    with colA:
        st.markdown('<div class="hero-card">', unsafe_allow_html=True)
        st.image(
            "https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?q=80&w=1200&auto=format&fit=crop",
            caption="Microscopy-inspired visual (Unsplash)",
            use_column_width=True,
        )
        st.markdown('</div>', unsafe_allow_html=True)
    with colB:
        st.markdown('<div class="hero-card">', unsafe_allow_html=True)
        st.image(
            "https://media.tenor.com/8b1mGfRrQmAAAAAd/chemistry-lab.gif",
            caption="Animated lab vibe (GIF)",
            use_column_width=True,
        )
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown(
    """
    ### Key features
    - **N/P ratio metrics** for quick quality checks.
    - **Bulk volumes**: auto-summed master mixes (ethanol ×1.5, aqueous ×1.2) and totals for multi-batch prep.
    - **History & export**: each run saved; download CSV for record-keeping.

    ### Quick start
    1. Run locally: `streamlit run 👋Homepage.py`
    2. Open a calculator page, enter parameters, and click **Calculate**.
    3. Expand **Bulk View details** in History to see multi-batch volumes.

    ### Enjoy the app!
    """
)
