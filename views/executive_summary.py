import streamlit as st
import pandas as pd
from datetime import datetime
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.llm_service import generate_executive_summary
from utils.helpers import (
    build_competitor_comparison, compute_sentiment_score,
    compute_nps_proxy, get_top_complaints, reviews_to_context_text
)
from utils.config import EMAMI_BRANDS as PRIMARY_BRANDS, CATEGORY_LABELS


def render_executive_summary(df: pd.DataFrame):
    st.markdown('<div class="page-title">Executive Summary</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">AI-generated strategic brief — ready to share with leadership</div>', unsafe_allow_html=True)

    if df.empty:
        st.warning("No data loaded.")
        return

    c1, c2, c3 = st.columns([2, 2, 1])
    with c1:
        sel_brands = st.multiselect(
            "Brands to include",
            sorted(df["brand"].unique().tolist()),
            default=sorted(df["brand"].unique().tolist()),
        )
    with c2:
        period = st.selectbox("Report period",
            ["Q1 2024", "Q2 2024", "H1 2024", "Full Year 2024", "YTD 2024"], index=4)
    with c3:
        st.markdown("<div style='margin-top:28px'></div>", unsafe_allow_html=True)
        gen_btn = st.button("Generate Report", use_container_width=True, key="gen_report")

    if not sel_brands:
        st.warning("Select at least one brand.")
        return

    filtered = df[df["brand"].isin(sel_brands)].copy()
    comp_df  = build_competitor_comparison(filtered)

    st.markdown("<div style='margin-top:20px'></div>", unsafe_allow_html=True)

    # KPI row
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Reviews in Report", len(filtered))
    m2.metric("Brands Covered",    len(sel_brands))
    m3.metric("Sentiment Score",   f"{compute_sentiment_score(filtered)} / 100")
    m4.metric("NPS Score",         f"{compute_nps_proxy(filtered):+.0f}")

    st.markdown("<div style='margin-top:18px'></div>", unsafe_allow_html=True)

    # Brand performance snapshot
    st.markdown("""<div class="chart-card">
        <div class="chart-title">Brand Performance Snapshot</div>
        <div class="chart-subtitle">Ratings and sentiment breakdown per brand</div>""",
        unsafe_allow_html=True)
    for _, row in comp_df.iterrows():
        is_p = row["brand"] in PRIMARY_BRANDS
        pill = ('<span class="brand-pill-primary">Primary</span>' if is_p
                else '<span class="brand-pill-competitor">Competitor</span>')
        st.markdown(f"""
        <div style="display:flex;justify-content:space-between;align-items:center;
                    padding:10px 0;border-bottom:1px solid #f1f5f9;font-size:0.83rem;">
            <div><b style="color:#0f172a;">{row['brand']}</b> &nbsp;{pill}</div>
            <div style="display:flex;gap:20px;color:#64748b;">
                <span>⭐ {row['avg_rating']}</span>
                <span style="color:#16a34a;">🟢 {row['positive_pct']}%</span>
                <span style="color:#dc2626;">🔴 {row['negative_pct']}%</span>
                <span>Score: <b style="color:#0f172a;">{row['sentiment_score']}</b></span>
            </div>
        </div>""", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Top issues
    neg_df = filtered[filtered["sentiment"] == "negative"]
    if not neg_df.empty:
        st.markdown("""<div class="chart-card">
            <div class="chart-title">Biggest Issues to Fix</div>
            <div class="chart-subtitle">Most frequent complaint categories in negative reviews</div>""",
            unsafe_allow_html=True)
        for _, row in get_top_complaints(filtered, n=5).iterrows():
            lbl = CATEGORY_LABELS.get(row["category"], row["category"].replace("_", " ").title())
            pct = round(row["count"] / len(neg_df) * 100, 1)
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:14px;margin-bottom:10px;">
                <div style="font-size:0.82rem;font-weight:600;color:#374151;min-width:150px;">{lbl}</div>
                <div style="flex:1;background:#fee2e2;border-radius:999px;height:8px;">
                    <div style="width:{pct}%;background:#ef4444;border-radius:999px;height:8px;"></div>
                </div>
                <div style="font-size:0.78rem;color:#94a3b8;min-width:110px;text-align:right;">
                    {row['count']} mentions ({pct}%)
                </div>
            </div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # AI brief
    st.markdown("""<div class="chart-card">
        <div class="chart-title">AI Executive Brief</div>
        <div class="chart-subtitle">Click Generate Report above — AI reads all data and writes a structured brief</div>""",
        unsafe_allow_html=True)

    if gen_btn:
        with st.spinner("Writing executive report…"):
            context = reviews_to_context_text(filtered, max_rows=80)
            summary = generate_executive_summary(context, sel_brands)
            st.session_state["last_summary"]   = summary
            st.session_state["summary_brands"] = sel_brands
            st.session_state["summary_period"] = period

    if st.session_state.get("last_summary"):
        now        = datetime.now().strftime("%B %d, %Y")
        brands_str = " · ".join(st.session_state["summary_brands"])
        st.markdown(f"""
        <div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:10px;padding:20px 24px;margin-top:10px;">
            <div style="display:flex;justify-content:space-between;padding-bottom:14px;
                        margin-bottom:16px;border-bottom:1px solid #e2e8f0;">
                <div>
                    <div style="font-size:0.95rem;font-weight:700;color:#0f172a;">Consumer Intelligence Report</div>
                    <div style="font-size:0.76rem;color:#94a3b8;margin-top:3px;">{brands_str} · {st.session_state['summary_period']}</div>
                </div>
                <div style="font-size:0.72rem;color:#94a3b8;text-align:right;line-height:1.7;">
                    Generated {now}<br><span style="font-weight:700;color:#374151;">CONFIDENTIAL</span>
                </div>
            </div>
            <div class="insight-box" style="background:#fff;border-left:4px solid #2563eb;">
                {st.session_state['last_summary'].replace(chr(10), '<br>')}
            </div>
        </div>""", unsafe_allow_html=True)
        st.markdown("<div style='margin-top:14px'></div>", unsafe_allow_html=True)
        report_txt = (
            f"FMCG Consumer Intelligence Report\n"
            f"Brands: {', '.join(st.session_state['summary_brands'])}\n"
            f"Period: {st.session_state['summary_period']}\n"
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
            f"{'='*60}\n\n{st.session_state['last_summary']}"
        )
        st.download_button("⬇  Download Report (.txt)", data=report_txt,
                           file_name=f"report_{datetime.now().strftime('%Y%m%d')}.txt",
                           mime="text/plain")
    else:
        st.markdown("""
        <div style="padding:36px;text-align:center;color:#94a3b8;font-size:0.84rem;
                    background:#f8fafc;border:1px dashed #e2e8f0;border-radius:10px;">
            <div style="font-size:1.8rem;margin-bottom:10px;">📋</div>
            Select brands above and click <b>Generate Report</b>.
        </div>""", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
