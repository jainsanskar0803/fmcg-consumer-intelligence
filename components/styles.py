import streamlit as st

def inject_css():
    st.markdown("""
    <style>
    /* Prevent sidebar from ever collapsing */
    [data-testid="collapsedControl"] { display: none !important; }
    section[data-testid="stSidebar"][aria-expanded="false"] {
        transform: none !important; margin-left: 0 !important;
        width: 240px !important; min-width: 240px !important;
    }
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }
    #MainMenu, footer, header { visibility: hidden; }

    .block-container {
        padding-top: 1.8rem !important;
        padding-bottom: 5rem !important;
        max-width: 1200px;
    }

    /* ══════════════════════
       SIDEBAR
    ══════════════════════ */
    section[data-testid="stSidebar"] {
        background: #0f172a !important;
        border-right: 1px solid #1e293b !important;
        min-width: 240px !important;
        max-width: 240px !important;
    }
    section[data-testid="stSidebar"] > div:first-child {
        padding: 0 !important;
    }
    /* make all text in sidebar light */
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] div,
    section[data-testid="stSidebar"] label {
        color: #94a3b8 !important;
    }

    /* NAV BUTTONS */
    section[data-testid="stSidebar"] .stButton > button {
        background: transparent !important;
        border: none !important;
        color: #94a3b8 !important;
        text-align: left !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
        padding: 9px 16px !important;
        border-radius: 8px !important;
        width: 100% !important;
        margin: 1px 4px !important;
        box-shadow: none !important;
        transition: all 0.15s !important;
    }
    section[data-testid="stSidebar"] .stButton > button:hover {
        background: #1e293b !important;
        color: #f1f5f9 !important;
    }
    section[data-testid="stSidebar"] .stButton > button:focus {
        box-shadow: none !important;
        outline: none !important;
    }

    /* MULTISELECT in sidebar */
    section[data-testid="stSidebar"] .stMultiSelect > div > div {
        background: #1e293b !important;
        border-color: #334155 !important;
        border-radius: 8px !important;
    }
    section[data-testid="stSidebar"] .stMultiSelect span[data-baseweb="tag"] {
        background: #334155 !important;
        border-radius: 6px !important;
        font-size: 0.72rem !important;
    }

    /* ── sidebar custom elements ── */
    .sb-logo {
        display: flex; align-items: center; gap: 10px;
        padding: 20px 16px 16px 16px;
        border-bottom: 1px solid #1e293b;
        margin-bottom: 16px;
    }
    .sb-logo-icon {
        background: #2563eb; border-radius: 10px;
        width: 40px; height: 40px; flex-shrink: 0;
        display: flex; align-items: center; justify-content: center;
        font-size: 1.2rem;
    }
    .sb-brand-name {
        font-size: 1rem; font-weight: 800;
        color: #f1f5f9 !important; letter-spacing: -0.01em; line-height: 1.1;
    }
    .sb-brand-sub {
        font-size: 0.58rem; font-weight: 700; letter-spacing: 0.13em;
        text-transform: uppercase; color: #475569 !important;
    }
    .sb-label {
        font-size: 0.6rem; font-weight: 700; letter-spacing: 0.12em;
        text-transform: uppercase; color: #475569 !important;
        padding: 0 16px; margin-bottom: 6px; display: block;
    }
    .sb-divider { border-top: 1px solid #1e293b; margin: 12px 0; }

    .sb-active-nav {
        background: #2563eb !important;
        border-radius: 8px;
        padding: 9px 16px;
        margin: 1px 4px;
        font-size: 0.85rem; font-weight: 600;
        color: #ffffff !important;
        cursor: default;
    }

    .sb-status-row {
        display: flex; align-items: center; gap: 8px;
        font-size: 0.78rem; color: #94a3b8 !important;
        padding: 3px 16px;
    }
    .sb-dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }
    .sb-dot-green  { background: #22c55e; }
    .sb-dot-red    { background: #ef4444; }
    .sb-dot-gray   { background: #475569; }
    .sb-badge {
        font-size: 0.6rem; font-weight: 800; padding: 1px 6px;
        border-radius: 4px; margin-left: 4px; letter-spacing: 0.03em;
    }
    .sb-badge-orange { background: #f97316; color: #fff !important; }
    .sb-badge-blue   { background: #2563eb; color: #fff !important; }

    .sb-version {
        padding: 14px 16px; font-size: 0.72rem;
        color: #334155 !important; display: flex; align-items: center; gap: 8px;
        border-top: 1px solid #1e293b; margin-top: 10px;
    }

    /* ══════════════════════
       MAIN CONTENT
    ══════════════════════ */
    .page-title {
        font-size: 1.65rem; font-weight: 800;
        color: #0f172a; letter-spacing: -0.03em; margin-bottom: 2px;
    }
    .page-subtitle { font-size: 0.82rem; color: #94a3b8; margin-bottom: 22px; }

    /* KPI cards */
    .kpi-card {
        background: #fff; border: 1px solid #e2e8f0; border-radius: 14px;
        padding: 18px 20px; box-shadow: 0 1px 4px rgba(0,0,0,0.06); min-height: 130px;
    }
    .kpi-icon {
        width: 36px; height: 36px; border-radius: 10px;
        display: flex; align-items: center; justify-content: center;
        font-size: 1rem; margin-bottom: 8px;
    }
    .kpi-icon-blue   { background: #eff6ff; }
    .kpi-icon-amber  { background: #fffbeb; }
    .kpi-icon-green  { background: #f0fdf4; }
    .kpi-icon-purple { background: #faf5ff; }
    .kpi-icon-teal   { background: #f0fdfa; }
    .kpi-label {
        font-size: 0.61rem; font-weight: 700; text-transform: uppercase;
        letter-spacing: 0.09em; color: #94a3b8; margin-bottom: 4px;
    }
    .kpi-value {
        font-size: 1.8rem; font-weight: 800;
        color: #0f172a; line-height: 1.1; letter-spacing: -0.02em;
    }
    .kpi-sub { font-size: 0.7rem; color: #94a3b8; margin-top: 4px; }
    .kpi-sub-green { color: #16a34a !important; font-weight: 600; }
    .kpi-sub-red   { color: #dc2626 !important; font-weight: 600; }

    /* Chart card */
    .chart-card {
        background: #fff; border: 1px solid #e2e8f0; border-radius: 14px;
        padding: 20px 22px 14px 22px;
        box-shadow: 0 1px 4px rgba(0,0,0,0.05); margin-bottom: 20px;
    }
    .chart-title  { font-size: 0.92rem; font-weight: 700; color: #0f172a; margin-bottom: 3px; }
    .chart-subtitle { font-size: 0.75rem; color: #94a3b8; margin-bottom: 14px; }

    /* Insight box */
    .insight-box {
        background: #f8fafc; border-left: 4px solid #3b82f6;
        border-radius: 0 10px 10px 0; padding: 18px 22px;
        font-size: 0.87rem; line-height: 1.85; color: #1e293b; margin: 14px 0;
    }

    /* Sentiment tags */
    .tag-positive { display:inline-block; background:#f0fdf4; border:1px solid #bbf7d0; color:#15803d; font-size:0.68rem; font-weight:700; padding:2px 10px; border-radius:999px; }
    .tag-negative { display:inline-block; background:#fef2f2; border:1px solid #fecaca; color:#dc2626; font-size:0.68rem; font-weight:700; padding:2px 10px; border-radius:999px; }
    .tag-mixed    { display:inline-block; background:#fffbeb; border:1px solid #fde68a; color:#b45309; font-size:0.68rem; font-weight:700; padding:2px 10px; border-radius:999px; }

    /* Review rows */
    .review-row { border-bottom:1px solid #f1f5f9; padding:13px 0; font-size:0.84rem; color:#334155; line-height:1.6; }
    .review-row:last-child { border-bottom:none; }
    .review-brand { font-size:0.67rem; font-weight:700; color:#94a3b8; text-transform:uppercase; letter-spacing:0.06em; margin-bottom:4px; }
    .review-meta  { margin-top:6px; display:flex; align-items:center; gap:8px; }

    /* Brand pills */
    .brand-pill-primary    { display:inline-block; background:#eff6ff; border:1px solid #bfdbfe; color:#1d4ed8; font-weight:700; font-size:0.68rem; padding:2px 10px; border-radius:999px; }
    .brand-pill-competitor { display:inline-block; background:#f8fafc; border:1px solid #e2e8f0; color:#475569; font-weight:700; font-size:0.68rem; padding:2px 10px; border-radius:999px; }

    /* Main area buttons */
    .stButton > button {
        background: #2563eb !important; color: #fff !important;
        border: none !important; border-radius: 8px !important;
        font-size: 0.83rem !important; font-weight: 600 !important;
        padding: 8px 18px !important; transition: background 0.15s !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.12) !important;
    }
    .stButton > button:hover { background: #1d4ed8 !important; }

    .stDownloadButton > button {
        background: #2563eb !important; color: #fff !important;
        border: none !important; border-radius: 8px !important;
        font-weight: 600 !important; font-size: 0.83rem !important;
    }

    /* Metric cards */
    div[data-testid="stMetric"] {
        background: #fff; border: 1px solid #e2e8f0; border-radius: 12px;
        padding: 16px 18px; box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }
    div[data-testid="stMetric"] label {
        font-size: 0.66rem !important; font-weight: 700 !important;
        text-transform: uppercase !important; letter-spacing: 0.08em !important;
        color: #94a3b8 !important;
    }
    div[data-testid="stMetricValue"] { font-size:1.6rem !important; font-weight:800 !important; color:#0f172a !important; }

    /* Inputs */
    .stTextArea > div > textarea { border-radius: 8px; border: 1px solid #e2e8f0; font-size: 0.85rem; }
    .stSelectbox > div > div { border-radius: 8px !important; }

    /* Footer */
    .app-footer {
        position: fixed; bottom: 0; left: 0; right: 0;
        background: rgba(255,255,255,0.96); backdrop-filter: blur(4px);
        border-top: 1px solid #e2e8f0; padding: 9px 32px;
        font-size: 0.72rem; color: #94a3b8; z-index: 100;
        display: flex; align-items: center; gap: 6px;
    }
    .footer-divider { margin: 0 8px; color: #e2e8f0; }
    </style>
    """, unsafe_allow_html=True)
