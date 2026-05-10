import streamlit as st
import pandas as pd
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.data_loader import load_uploaded_csv, load_txt_file, load_demo_data
from services.mongodb_service import save_upload_metadata, get_upload_history, is_mongodb_connected
from utils.config import ALL_BRANDS, EMAMI_BRANDS


def render_upload():
    st.markdown('<div class="page-title">Upload Reviews</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Load your own review data or use a built-in demo dataset</div>', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📁  Upload File", "🗂  Demo Datasets", "🕑  Upload History"])

    # ── Tab 1: Upload File ───────────────────────────────────────────────────
    with tab1:
        st.markdown("""<div class="chart-card">
            <div class="chart-title">Upload a CSV or TXT file</div>
            <div class="chart-subtitle">CSV needs at least: <b>review_text</b>, <b>rating</b> (1–5), <b>sentiment</b> (positive / negative / mixed)</div>""",
            unsafe_allow_html=True)

        uploaded = st.file_uploader("Drop file here", type=["csv", "txt"], label_visibility="collapsed")
        if uploaded:
            ftype = uploaded.name.split(".")[-1].lower()
            with st.spinner("Reading file…"):
                df = load_uploaded_csv(uploaded) if ftype == "csv" else load_txt_file(uploaded)
            if not df.empty:
                st.success(f"✅ Loaded **{len(df)} reviews** from `{uploaded.name}`")
                st.dataframe(df.head(10), use_container_width=True)
                c1, c2, c3 = st.columns(3)
                c1.metric("Total Rows", len(df))
                c2.metric("Brands",     df["brand"].nunique() if "brand" in df.columns else "—")
                c3.metric("Avg Rating", round(df["rating"].mean(), 2) if "rating" in df.columns else "—")
                st.markdown("<div style='margin-top:14px'></div>", unsafe_allow_html=True)
                if st.button("✅  Use this as active dataset", key="use_upload"):
                    st.session_state.df              = df
                    st.session_state.data_source     = uploaded.name
                    st.session_state.rag_built       = False
                    st.session_state.selected_brands = (df["brand"].unique().tolist()
                                                        if "brand" in df.columns else [])
                    save_upload_metadata(uploaded.name, ftype, len(df),
                                         df["brand"].unique().tolist() if "brand" in df.columns else [])
                    st.success("Loaded! Switch to Dashboard.")
                    st.rerun()
            else:
                st.error("Could not read file. Check the format.")
        else:
            st.markdown("""
            <div style="padding:48px;text-align:center;color:#94a3b8;background:#f8fafc;
                        border:2px dashed #e2e8f0;border-radius:10px;margin-top:8px;">
                <div style="font-size:2rem;margin-bottom:8px;">📂</div>
                Drag and drop a CSV or TXT file, or click above to browse
            </div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # Template download
        st.markdown("""<div class="chart-card">
            <div class="chart-title">Download CSV Template</div>
            <div class="chart-subtitle">Use this to format your own review data correctly</div>""",
            unsafe_allow_html=True)
        template_csv = (
            "review_text,rating,sentiment,brand,product,category,date\n"
            "Great product!,5,positive,Brand A,Product X,general,2024-01-01\n"
            "Packaging issue,3,mixed,Brand A,Product X,packaging,2024-01-02\n"
        )
        st.download_button("⬇  Download template", data=template_csv,
                           file_name="review_template.csv", mime="text/csv")
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Tab 2: Demo Datasets ─────────────────────────────────────────────────
    with tab2:
        st.markdown("""<div class="chart-card">
            <div class="chart-title">Built-in Demo Datasets</div>
            <div class="chart-subtitle">Pre-loaded realistic FMCG reviews including Hinglish — click Load to use any dataset</div>""",
            unsafe_allow_html=True)
        demo_df  = load_demo_data()
        datasets = [
            {
                "name": "Full FMCG Dataset",
                "desc": "All 6 brands — best for competitor analysis",
                "brands": ALL_BRANDS,
                "rows": len(demo_df),
            },
            {
                "name": "Primary Portfolio",
                "desc": "Navratna Oil + Kesh King + BoroPlus",
                "brands": EMAMI_BRANDS,
                "rows": len(demo_df[demo_df["brand"].isin(EMAMI_BRANDS)]),
            },
            {
                "name": "Competitors Only",
                "desc": "Dabur, Mamaearth, Himalaya for benchmarking",
                "brands": ["Dabur Amla", "Mamaearth Onion Oil", "Himalaya Hair Oil"],
                "rows": len(demo_df[demo_df["brand"].isin(
                    ["Dabur Amla", "Mamaearth Onion Oil", "Himalaya Hair Oil"])]),
            },
            {
                "name": "Navratna Oil Focus",
                "desc": "Single-product deep dive",
                "brands": ["Navratna Oil"],
                "rows": len(demo_df[demo_df["brand"] == "Navratna Oil"]),
            },
        ]
        for ds in datasets:
            ci, cb = st.columns([5, 1])
            with ci:
                st.markdown(f"""
                <div style="padding:12px 0;border-bottom:1px solid #f1f5f9;">
                    <div style="font-size:0.9rem;font-weight:700;color:#0f172a;">{ds['name']}</div>
                    <div style="font-size:0.79rem;color:#64748b;margin-top:2px;">
                        {ds['desc']} · {ds['rows']} reviews
                    </div>
                </div>""", unsafe_allow_html=True)
            with cb:
                st.markdown("<div style='margin-top:14px'></div>", unsafe_allow_html=True)
                if st.button("Load", key=f"load_{ds['name']}", use_container_width=True):
                    st.session_state.df              = demo_df[demo_df["brand"].isin(ds["brands"])].copy()
                    st.session_state.selected_brands = ds["brands"]
                    st.session_state.data_source     = ds["name"]
                    st.session_state.rag_built       = False
                    st.session_state.active_page     = "Dashboard"
                    st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Tab 3: Upload History ────────────────────────────────────────────────
    with tab3:
        st.markdown("""<div class="chart-card">
            <div class="chart-title">Upload History</div>
            <div class="chart-subtitle">Every file upload is logged in MongoDB — useful for tracking what data has been analysed</div>""",
            unsafe_allow_html=True)
        if not is_mongodb_connected():
            st.info(
                "**MongoDB not running.** Start it to enable upload history.\n\n"
                "- Mac: `brew services start mongodb-community`\n"
                "- Linux: `sudo systemctl start mongod`\n"
                "- Cloud: add MongoDB Atlas URI to `.env` as `MONGO_URI`"
            )
        else:
            history = get_upload_history(20)
            if not history:
                st.markdown('<div style="color:#94a3b8;font-size:0.84rem;">No uploads yet.</div>',
                            unsafe_allow_html=True)
            else:
                for item in history:
                    ts     = str(item.get("uploaded_at", ""))[:16]
                    brands = ", ".join(item.get("brands", []))
                    st.markdown(f"""
                    <div class="review-row">
                        <div style="font-size:0.84rem;font-weight:600;color:#334155;">{item.get('filename','')}</div>
                        <div style="font-size:0.76rem;color:#64748b;">
                            {item.get('row_count',0)} rows · {item.get('file_type','').upper()} · {ts}
                        </div>
                        <div style="font-size:0.72rem;color:#94a3b8;">{brands}</div>
                    </div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
