import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.helpers import build_competitor_comparison, compute_sentiment_score
from utils.config import EMAMI_BRANDS as PRIMARY_BRANDS
from components.charts import competitor_radar, brand_sentiment_bar, sentiment_donut

_C = {"displayModeBar": False}


def render_competitor(df: pd.DataFrame):
    st.markdown('<div class="page-title">Competitor Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Side-by-side comparison of all brands in your dataset</div>', unsafe_allow_html=True)

    if df.empty:
        st.warning("No data loaded.")
        return

    comp_df = build_competitor_comparison(df)
    tab1, tab2 = st.tabs(["📊  Overview", "🔍  Brand Deep-Dive"])

    # ── Tab 1: Overview ──────────────────────────────────────────────────────
    with tab1:
        st.markdown("""<div class="chart-card">
            <div class="chart-title">Brand Scorecard</div>
            <div class="chart-subtitle">Quick comparison — ratings, sentiment, and NPS at a glance</div>""",
            unsafe_allow_html=True)
        for _, row in comp_df.iterrows():
            is_p  = row["brand"] in PRIMARY_BRANDS
            pill  = ('<span class="brand-pill-primary">Primary</span>' if is_p
                     else '<span class="brand-pill-competitor">Competitor</span>')
            pw, nw, mw = int(row["positive_pct"]), int(row["negative_pct"]), int(row["mixed_pct"])
            st.markdown(f"""
            <div style="padding:14px 0;border-bottom:1px solid #f1f5f9;">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;">
                    <div>
                        <span style="font-size:0.9rem;font-weight:700;color:#0f172a;">{row['brand']}</span>
                        &nbsp;&nbsp;{pill}
                    </div>
                    <div style="display:flex;gap:22px;font-size:0.79rem;color:#64748b;">
                        <span>⭐ <b style="color:#0f172a;">{row['avg_rating']}</b></span>
                        <span>📝 <b style="color:#0f172a;">{row['total_reviews']}</b> reviews</span>
                        <span>Score: <b style="color:#0f172a;">{row['sentiment_score']}</b>/100</span>
                        <span>NPS: <b style="color:#0f172a;">{row['nps_proxy']:+.0f}</b></span>
                    </div>
                </div>
                <div style="display:flex;height:8px;border-radius:999px;overflow:hidden;gap:2px;">
                    <div style="width:{pw}%;background:#22c55e;border-radius:999px 0 0 999px;"></div>
                    <div style="width:{mw}%;background:#f59e0b;"></div>
                    <div style="width:{nw}%;background:#ef4444;border-radius:0 999px 999px 0;"></div>
                </div>
                <div style="display:flex;gap:16px;margin-top:6px;font-size:0.7rem;color:#64748b;">
                    <span>🟢 {row['positive_pct']}% positive</span>
                    <span>🟡 {row['mixed_pct']}% mixed</span>
                    <span>🔴 {row['negative_pct']}% negative</span>
                </div>
            </div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            st.markdown("""<div class="chart-card">
                <div class="chart-title">Sentiment Side by Side</div>
                <div class="chart-subtitle">Positive, mixed, and negative share per brand</div>""",
                unsafe_allow_html=True)
            st.plotly_chart(brand_sentiment_bar(df), width='stretch', config=_C, key="comp_bs")
            st.markdown("</div>", unsafe_allow_html=True)

        with c2:
            st.markdown("""<div class="chart-card">
                <div class="chart-title">Performance Radar</div>
                <div class="chart-subtitle">Bigger shape = better across rating, positivity, and score</div>""",
                unsafe_allow_html=True)
            st.plotly_chart(competitor_radar(comp_df), width='stretch', config=_C, key="comp_radar")
            st.markdown("</div>", unsafe_allow_html=True)

        # Heatmap
        st.markdown("""<div class="chart-card">
            <div class="chart-title">Category Ratings Heatmap</div>
            <div class="chart-subtitle">Green = rated well · Red = area of concern · 0 = no data</div>""",
            unsafe_allow_html=True)
        pivot = (df.pivot_table(index="brand", columns="category", values="rating", aggfunc="mean")
                   .round(2).fillna(0))
        fig3 = go.Figure(go.Heatmap(
            z=pivot.values,
            x=[c.replace("_", " ").title() for c in pivot.columns],
            y=pivot.index,
            colorscale=[[0, "#fef2f2"], [0.5, "#fef9c3"], [1, "#f0fdf4"]],
            text=pivot.values.round(1),
            texttemplate="%{text}", textfont={"size": 10},
            hovertemplate="%{y} — %{x}<br>Avg rating: %{z:.1f}<extra></extra>",
        ))
        fig3.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter,sans-serif", size=11), height=310,
            margin=dict(l=20, r=20, t=10, b=60), xaxis=dict(tickangle=-35),
        )
        st.plotly_chart(fig3, width='stretch', config=_C, key="heatmap")
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Tab 2: Brand Deep-Dive ────────────────────────────────────────────────
    with tab2:
        st.markdown('<div class="section-title" style="margin-bottom:10px;">Pick a brand to explore</div>',
                    unsafe_allow_html=True)
        brand_opts = sorted(df["brand"].unique().tolist())
        sel_brand  = st.selectbox("Select brand", brand_opts, label_visibility="collapsed", key="deep_brand")
        bdf        = df[df["brand"] == sel_brand].copy()

        b1, b2, b3, b4 = st.columns(4)
        b1.metric("Total Reviews",    len(bdf))
        b2.metric("Average Rating",   round(bdf["rating"].mean(), 2))
        b3.metric("Sentiment Score",  compute_sentiment_score(bdf))
        b4.metric("Positive Reviews", len(bdf[bdf["sentiment"] == "positive"]))

        st.markdown("<div style='margin-top:18px'></div>", unsafe_allow_html=True)
        ca, cb = st.columns(2)

        with ca:
            st.markdown("""<div class="chart-card">
                <div class="chart-title">Review Topics</div>
                <div class="chart-subtitle">What customers are mainly talking about</div>""",
                unsafe_allow_html=True)
            cat_counts = (bdf.groupby("category").size()
                          .reset_index(name="count")
                          .sort_values("count", ascending=False))
            cat_counts["category"] = cat_counts["category"].str.replace("_", " ").str.title()
            fig_cat = px.bar(cat_counts.head(8), x="count", y="category", orientation="h",
                             color_discrete_sequence=["#3b82f6"], text="count")
            fig_cat.update_traces(textposition="outside", marker_line_width=0)
            fig_cat.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                height=280, showlegend=False,
                font=dict(family="Inter,sans-serif", size=11),
                margin=dict(l=10, r=30, t=10, b=10),
                xaxis=dict(title="", gridcolor="#f1f5f9"),
                yaxis=dict(title=""),
            )
            st.plotly_chart(fig_cat, width='stretch', config=_C, key=f"bc_{sel_brand}")
            st.markdown("</div>", unsafe_allow_html=True)

        with cb:
            st.markdown("""<div class="chart-card">
                <div class="chart-title">Sentiment Split</div>
                <div class="chart-subtitle">Share of positive, negative, and mixed</div>""",
                unsafe_allow_html=True)
            st.plotly_chart(sentiment_donut(bdf), width='stretch', config=_C, key=f"bd_{sel_brand}")
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("""<div class="chart-card">
            <div class="chart-title">Sample Reviews</div>
            <div class="chart-subtitle">A random selection of actual customer feedback</div>""",
            unsafe_allow_html=True)
        for _, row in bdf.sample(min(5, len(bdf)), random_state=1).iterrows():
            tag = f"tag-{row['sentiment']}"
            st.markdown(f"""
            <div class="review-row">
                <div class="review-brand">{str(row.get('category','')).replace('_',' ').title()}</div>
                <div>{row['review_text']}</div>
                <div class="review-meta">
                    <span class="{tag}">{row['sentiment'].capitalize()}</span>
                    <span style="font-size:0.72rem;color:#94a3b8;">⭐ {row['rating']} / 5</span>
                </div>
            </div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
