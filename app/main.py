import os
import pandas as pd
import streamlit as st


print("System: ONLINE")

from app.visuals import render_light_cones
from core.physics import GodelUniverse
from core.simulation import run_batch_simulation


st.set_page_config(
    page_title="ETERNAL_RETURN: Project Nietzsche",
    page_icon="🌀",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    body {
        background-color: #0e1117;
        color: #f5f5f5;
    }
    .stApp {
        background-color: #0e1117;
        color: #f5f5f5;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
    }
    .stTabs [data-baseweb="tab"] {
        background: #111827;
        padding: 0.75rem 1rem;
        border-radius: 0.5rem 0.5rem 0 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🌀 ETERNAL_RETURN: Project Nietzsche")
st.caption("Gödel geometry × Nietzschean time × Information-theoretic constraints")

with st.sidebar:
    st.header("Controls")
    omega = st.slider("Universal Rotation (ω)", 0.1, 2.0, 0.5, 0.1)
    max_complexity = st.slider("Max Complexity (Entropy)", 50, 500, 200, 10)
    noise_level = st.slider("Noise Level", 0.0, 0.8, 0.5, 0.05)
    run_sim = st.button("RUN MONTE CARLO SIMULATION")

if "latest_results" not in st.session_state:
    st.session_state["latest_results"] = None

if run_sim:
    with st.spinner("Running Monte Carlo simulation..."):
        st.session_state["latest_results"] = run_batch_simulation(
            max_complexity=max_complexity,
            iterations=300,
            noise_level=noise_level,
        )
else:
    if st.session_state["latest_results"] is None:
        if os.path.exists("simulation_results.csv"):
            st.session_state["latest_results"] = pd.read_csv("simulation_results.csv")

tabs = st.tabs(["Spacetime Geometry", "Information Constraints"])

with tabs[0]:
    st.subheader("Spacetime Geometry: Light Cone Tipping")
    fig = render_light_cones(omega)
    st.plotly_chart(fig, use_container_width=True)

    gu = GodelUniverse(omega=omega)
    r_crit = gu.find_critical_radius()
    if r_crit is not None:
        st.markdown(f"**Critical Radius** (approx.): `r_crit ≈ {r_crit:.3f}`")
    else:
        st.markdown("**Critical Radius:** No CTC region detected in scan range.")

with tabs[1]:
    st.subheader("Information Constraints: Entropy vs Eternal Return")
    df = st.session_state.get("latest_results")

    if df is not None:
        chart_data = df.set_index("complexity")["survival_rate"]
        st.line_chart(chart_data)
        last_row = df.iloc[-1]
        surv = float(last_row["survival_rate"])
        st.markdown(
            f"**Survival Rate at Complexity {int(last_row['complexity'])}:** {surv:.4f}"
        )

        if surv < 0.001:
            st.markdown(
                "🟥 **Status:** ETERNAL RETURN IMPOSSIBLE FOR THIS COMPLEXITY (ENTROPY TOO HIGH)."
            )
        elif surv > 0.5:
            st.markdown(
                "🟩 **Status:** RETURN REGION DETECTED (LOW ENTROPY LOOP)."
            )
        else:
            st.markdown(
                "🟨 **Status:** RETURN HIGHLY SUPPRESSED BUT NOT IMPOSSIBLE."
            )
    else:
        st.info("Run the Monte Carlo simulation to see entropy constraints.")
