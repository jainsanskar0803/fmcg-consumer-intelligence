import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

st.set_page_config(
    page_title="FMCG Consumer Intelligence",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Force sidebar to stay permanently visible ──────────────────────────────
# Streamlit collapses sidebar after st.rerun() — this CSS prevents that.
st.markdown("""
<style>
[data-testid="collapsedControl"] { display: none !important; }
section[data-testid="stSidebar"] {
    transform: none !important;
    width: 240px !important;
    min-width: 240px !important;
}
section[data-testid="stSidebar"][aria-expanded="false"] {
    transform: none !important;
    margin-left: 0 !important;
    width: 240px !important;
    min-width: 240px !important;
}
</style>
""", unsafe_allow_html=True)

from services.data_loader import load_demo_data
from utils.config import ALL_BRANDS
from components.styles import inject_css
from components.sidebar import render_sidebar
from views.dashboard import render_dashboard
from views.competitor import render_competitor
from views.ask_questions import render_ask_questions
from views.executive_summary import render_executive_summary
from views.upload import render_upload

inject_css()

# ── Session state defaults ─────────────────────────────────────────────────
defaults = {
    "active_page":     "Dashboard",
    "df":              None,
    "selected_brands": list(ALL_BRANDS),
    "data_source":     "Full Demo Dataset",
    "rag_built":       False,
    "chat_history":    [],
    "last_summary":    None,
    "summary_brands":  [],
    "summary_period":  "",
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

if st.session_state.df is None:
    st.session_state.df = load_demo_data()

render_sidebar()

page = st.session_state.active_page
df   = st.session_state.df

if   page == "Dashboard":           render_dashboard(df)
elif page == "Competitor Analysis": render_competitor(df)
elif page == "Ask Questions":       render_ask_questions(df)
elif page == "Executive Summary":   render_executive_summary(df)
elif page == "Upload Reviews":      render_upload()

st.markdown("""
<div class="app-footer">
    <span>FMCG Consumer Intelligence Platform</span>
    <span class="footer-divider">·</span>
    <span>Built by Sanskar</span>
</div>
""", unsafe_allow_html=True)
