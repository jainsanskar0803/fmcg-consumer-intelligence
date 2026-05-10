import streamlit as st
import pandas as pd
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.helpers import (
    compute_sentiment_score, compute_nps_proxy,
    extract_keywords_frequency, get_top_complaints
)
from utils.config import CATEGORY_LABELS
from components.charts import (
    sentiment_donut, rating_bar, brand_sentiment_bar,
    avg_rating_brand, timeline_sentiment
)

_C = {"displayModeBar": False}


def render_dashboard(df: pd.DataFrame):
    sel = st.session_state.get("selected_brands", [])
    if sel:
        df = df[df["brand"].isin(sel)].copy()

    if df.empty:
        st.warning("No reviews match your filter. Use the sidebar to change brand selection.")
        return

    # ── Header ──────────────────────────────────────────────────────────────
    h1, h2 = st.columns([4, 1])
    with h1:
        st.markdown('<div class="page-title">Consumer Intelligence Dashboard</div>', unsafe_allow_html=True)
        st.markdown('<div class="page-subtitle">Live view of customer reviews · India FMCG market</div>', unsafe_allow_html=True)
    with h2:
        st.markdown("<div style='margin-top:12px'></div>", unsafe_allow_html=True)
        csv = df.to_csv(index=False)
        st.download_button("⬇ Export Report", data=csv,
                           file_name="fmcg_reviews.csv", mime="text/csv",
                           use_container_width=True)

    # ── KPIs ─────────────────────────────────────────────────────────────────
    total   = len(df)
    avg_r   = round(df["rating"].mean(), 2)
    score   = compute_sentiment_score(df)
    nps     = compute_nps_proxy(df)
    pos_pct = round(len(df[df["sentiment"] == "positive"]) / total * 100, 1)
    neg_pct = round(len(df[df["sentiment"] == "negative"]) / total * 100, 1)

    k1, k2, k3, k4, k5 = st.columns(5)

    with k1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon kpi-icon-blue">💬</div>
            <div class="kpi-label">Total Reviews</div>
            <div class="kpi-value">{total:,}</div>
            <div class="kpi-sub">All Selected Brands</div>
        </div>""", unsafe_allow_html=True)

    with k2:
        sub_cls = "kpi-sub-green" if avg_r >= 4 else ("kpi-sub-red" if avg_r < 3 else "kpi-sub")
        sub_txt = "Above Average" if avg_r >= 4 else ("Below Average" if avg_r < 3 else "Average")
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon kpi-icon-amber">⭐</div>
            <div class="kpi-label">Average Rating</div>
            <div class="kpi-value">{avg_r} / 5</div>
            <div class="kpi-sub {sub_cls}">{sub_txt}</div>
        </div>""", unsafe_allow_html=True)

    with k3:
        s_cls = "kpi-sub-green" if score >= 65 else ("kpi-sub-red" if score < 45 else "kpi-sub")
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon kpi-icon-green">😊</div>
            <div class="kpi-label">Sentiment Score</div>
            <div class="kpi-value">{score} / 100</div>
            <div class="kpi-sub {s_cls}">Overall Sentiment</div>
        </div>""", unsafe_allow_html=True)

    with k4:
        n_cls = "kpi-sub-green" if nps >= 20 else ("kpi-sub-red" if nps < 0 else "kpi-sub")
        n_txt = "Good" if nps >= 20 else ("Needs Work" if nps < 0 else "Fair")
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon kpi-icon-purple">📈</div>
            <div class="kpi-label">NPS Score</div>
            <div class="kpi-value">{nps:+.0f}</div>
            <div class="kpi-sub {n_cls}">{n_txt}</div>
        </div>""", unsafe_allow_html=True)

    with k5:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon kpi-icon-teal">👍</div>
            <div class="kpi-label">Positive Reviews</div>
            <div class="kpi-value">{pos_pct}%</div>
            <div class="kpi-sub kpi-sub-red">↑ {neg_pct}% negative</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div style='margin-top:22px'></div>", unsafe_allow_html=True)

    # ── Row 1: Sentiment by Brand + Avg Rating ───────────────────────────────
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""<div class="chart-card">
            <div class="chart-title">Sentiment by Brand</div>
            <div class="chart-subtitle">Distribution of positive, mixed &amp; negative reviews</div>""",
            unsafe_allow_html=True)
        st.plotly_chart(brand_sentiment_bar(df), width='stretch', config=_C, key="bsb")
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown("""<div class="chart-card">
            <div class="chart-title">Average Rating by Brand</div>
            <div class="chart-subtitle">Ranked from highest to lowest rated</div>""",
            unsafe_allow_html=True)
        st.plotly_chart(avg_rating_brand(df), width='stretch', config=_C, key="arb")
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Row 2: Donut + Star spread ───────────────────────────────────────────
    c3, c4 = st.columns(2)
    pos_n = len(df[df["sentiment"] == "positive"])
    neg_n = len(df[df["sentiment"] == "negative"])
    mix_n = len(df[df["sentiment"] == "mixed"])

    with c3:
        st.markdown("""<div class="chart-card">
            <div class="chart-title">How Customers Feel Overall</div>
            <div class="chart-subtitle">Share of positive, negative &amp; mixed reviews</div>""",
            unsafe_allow_html=True)
        st.plotly_chart(sentiment_donut(df), width='stretch', config=_C, key="sd")
        st.markdown(f"""
        <div style="display:flex;gap:20px;justify-content:center;font-size:0.76rem;
                    margin-top:4px;padding-bottom:4px;">
            <span>🟢 Positive ({round(pos_n/total*100,1)}%)</span>
            <span>🟡 Mixed ({round(mix_n/total*100,1)}%)</span>
            <span>🔴 Negative ({round(neg_n/total*100,1)}%)</span>
        </div></div>""", unsafe_allow_html=True)

    with c4:
        st.markdown("""<div class="chart-card">
            <div class="chart-title">Star Rating Spread</div>
            <div class="chart-subtitle">How many reviews got each star rating (1–5)</div>""",
            unsafe_allow_html=True)
        st.plotly_chart(rating_bar(df), width='stretch', config=_C, key="rb")
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Row 3: Complaints + Word cloud ───────────────────────────────────────
    c5, c6 = st.columns(2)

    with c5:
        st.markdown("""<div class="chart-card">
            <div class="chart-title">What Customers Complain About Most</div>
            <div class="chart-subtitle">Top categories mentioned in negative reviews</div>""",
            unsafe_allow_html=True)
        neg_df = df[df["sentiment"] == "negative"]
        if not neg_df.empty:
            top_c   = get_top_complaints(df, n=5)
            total_n = len(neg_df)
            cols_c  = st.columns(min(5, len(top_c)))
            for i, (_, row) in enumerate(top_c.iterrows()):
                lbl = CATEGORY_LABELS.get(row["category"],
                      row["category"].replace("_", " ").title())
                pct = round(row["count"] / total_n * 100)
                with cols_c[i]:
                    st.markdown(f"""
                    <div style="background:#fef2f2;border:1px solid #fecaca;border-radius:10px;
                                padding:12px 8px;text-align:center;">
                        <div style="font-size:1.1rem;margin-bottom:4px;">🔴</div>
                        <div style="font-size:0.7rem;font-weight:600;color:#374151;margin-bottom:4px;">{lbl}</div>
                        <div style="font-size:1rem;font-weight:800;color:#dc2626;">{pct}%</div>
                    </div>""", unsafe_allow_html=True)
        else:
            st.info("No negative reviews in current selection.")
        st.markdown("</div>", unsafe_allow_html=True)

    with c6:
        st.markdown("""<div class="chart-card">
            <div class="chart-title">Words Customers Use Most Often</div>
            <div class="chart-subtitle">Bigger word = appears more often in reviews</div>""",
            unsafe_allow_html=True)
        word_freq = extract_keywords_frequency(df, top_n=20)
        if word_freq:
            max_c   = max(word_freq.values())
            palette = ["#1d4ed8","#3b82f6","#60a5fa","#0f172a","#374151","#f97316","#16a34a"]
            words_html = ""
            for i, (w, cnt) in enumerate(word_freq.items()):
                size  = 0.76 + (cnt / max_c) * 0.95
                color = palette[i % len(palette)]
                weight = 600 if size > 1.2 else 400
                words_html += (f'<span style="font-size:{size:.2f}rem;color:{color};'
                               f'font-weight:{weight};margin:4px 5px;display:inline-block;">{w}</span>')
            st.markdown(f'<div style="padding:8px 0;line-height:2.1;">{words_html}</div>',
                        unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Row 4: Trend ─────────────────────────────────────────────────────────
    st.markdown("""<div class="chart-card">
        <div class="chart-title">Sentiment Trend Over Time</div>
        <div class="chart-subtitle">Are customers getting happier or more frustrated month by month?</div>""",
        unsafe_allow_html=True)
    fig_trend = timeline_sentiment(df)
    if fig_trend:
        st.plotly_chart(fig_trend, width='stretch', config=_C, key="trend")
    else:
        st.info("Not enough date data to show trend.")
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Recent Reviews ────────────────────────────────────────────────────────
    st.markdown("""<div class="chart-card">
        <div class="chart-title">Latest Customer Reviews</div>
        <div class="chart-subtitle">Most recent feedback — useful for spotting new issues early</div>""",
        unsafe_allow_html=True)
    for _, row in df.sort_values("date", ascending=False).head(6).iterrows():
        tag  = f"tag-{row['sentiment']}"
        cat  = CATEGORY_LABELS.get(str(row.get("category", "")),
               str(row.get("category", "")).replace("_", " ").title())
        date = str(row.get("date", ""))[:10]
        st.markdown(f"""
        <div class="review-row">
            <div class="review-brand">{row['brand']} · {cat} · {date}</div>
            <div>{row['review_text']}</div>
            <div class="review-meta">
                <span class="{tag}">{row['sentiment'].capitalize()}</span>
                <span style="font-size:0.72rem;color:#94a3b8;">⭐ {row['rating']} / 5</span>
            </div>
        </div>""", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
