import streamlit as st

from app.visuals import render_light_cones

st.set_page_config(
    page_title="ETERNAL_RETURN: Project Nietzsche",
    page_icon="🌀",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(
    """
    <style>
    body {
        background-color: #0e1117;
        color: #f5f5f5;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("ETERNAL_RETURN: Project Nietzsche")
st.markdown("### System: ✅ ONLINE")
st.markdown("This is the genesis of the Eternal Return computational lab.")

omega = st.sidebar.slider("Universal Rotation ω", 0.1, 2.0, 0.5, 0.1)
st.subheader("Spacetime Geometry: Light Cone Tipping")
fig = render_light_cones(omega)
st.plotly_chart(fig, use_container_width=True)
