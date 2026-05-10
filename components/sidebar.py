import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.mongodb_service import is_mongodb_connected
from utils.config import ALL_BRANDS, EMAMI_BRANDS, GEMINI_API_KEY, GROQ_API_KEY

NAV_ITEMS = [
    ("🏠", "Dashboard"),
    ("📊", "Competitor Analysis"),
    ("💬", "Ask Questions"),
    ("📋", "Executive Summary"),
    ("⬆️", "Upload Reviews"),
]


def render_sidebar():
    with st.sidebar:

        # ── Logo ─────────────────────────────────────────────────────────────
        st.markdown("""
        <div class="sb-logo">
            <div class="sb-logo-icon">🛒</div>
            <div>
                <div class="sb-brand-name">FMCG</div>
                <div class="sb-brand-sub">Intelligence</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Navigation ────────────────────────────────────────────────────────
        st.markdown('<span class="sb-label">Navigation</span>', unsafe_allow_html=True)

        for icon, page in NAV_ITEMS:
            if st.session_state.get("active_page") == page:
                # Active page — styled highlight, non-clickable look
                st.markdown(f'<div class="sb-active-nav">{icon} &nbsp; {page}</div>',
                             unsafe_allow_html=True)
            else:
                if st.button(f"{icon}  {page}", key=f"nav_{page}", use_container_width=True):
                    st.session_state.active_page = page
                    st.rerun()

        st.markdown('<div class="sb-divider"></div>', unsafe_allow_html=True)

        # ── Brand Filter ──────────────────────────────────────────────────────
        st.markdown('<span class="sb-label">Brand Filter</span>', unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            if st.button("Primary", key="fp", use_container_width=True):
                st.session_state.selected_brands = list(EMAMI_BRANDS)
                st.rerun()
        with c2:
            if st.button("All Brands", key="fa", use_container_width=True):
                st.session_state.selected_brands = list(ALL_BRANDS)
                st.rerun()

        selected = st.multiselect(
            "brands",
            options=ALL_BRANDS,
            default=st.session_state.get("selected_brands", ALL_BRANDS),
            label_visibility="collapsed",
        )
        if selected != st.session_state.get("selected_brands"):
            st.session_state.selected_brands = selected
            st.rerun()

        if st.button("🗑  Clear All", key="clear_brands", use_container_width=True):
            st.session_state.selected_brands = []
            st.rerun()

        st.markdown('<div class="sb-divider"></div>', unsafe_allow_html=True)

        # ── System Status ─────────────────────────────────────────────────────
        st.markdown('<span class="sb-label">System Status</span>', unsafe_allow_html=True)

        mongo_ok = is_mongodb_connected()
        api_ok   = bool(GEMINI_API_KEY or GROQ_API_KEY)
        rag_ok   = st.session_state.get("rag_built", False)

        # AI provider badge
        if GROQ_API_KEY:
            ai_text  = "Groq API — Active"
            ai_badge = '<span class="sb-badge sb-badge-orange">Groq</span>'
        elif GEMINI_API_KEY:
            ai_text  = "Gemini API — Active"
            ai_badge = '<span class="sb-badge sb-badge-blue">G</span>'
        else:
            ai_text  = "AI — No Key Set"
            ai_badge = ""

        def dot(ok, gray=False):
            cls = "sb-dot-gray" if gray else ("sb-dot-green" if ok else "sb-dot-red")
            return f'<span class="sb-dot {cls}"></span>'

        st.markdown(f"""
        <div class="sb-status-row">{dot(mongo_ok)}<span>MongoDB — {'Connected' if mongo_ok else 'Offline'}</span></div>
        <div class="sb-status-row">{dot(api_ok)}<span>{ai_text}</span>{ai_badge}</div>
        <div class="sb-status-row">{dot(rag_ok, gray=not rag_ok)}<span>RAG Index — {'Ready' if rag_ok else 'Not Built'}</span></div>
        """, unsafe_allow_html=True)

        # ── Version ───────────────────────────────────────────────────────────
        df    = st.session_state.get("df")
        total = len(df) if df is not None and not df.empty else 0
        st.markdown(f"""
        <div class="sb-version">
            <span>📊</span>
            <span>v1.0 · FMCG Analytics · {total} reviews</span>
        </div>
        """, unsafe_allow_html=True)
