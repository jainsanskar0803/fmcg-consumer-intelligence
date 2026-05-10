import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from utils.config import SENTIMENT_COLORS, CATEGORY_LABELS

_FONT   = dict(family="Inter, sans-serif", size=12, color="#334155")
_TRANS  = "rgba(0,0,0,0)"
_GRID   = "#f1f5f9"
_CFG    = {"displayModeBar": False}


def _base(title="", height=320):
    return dict(
        title=dict(text=title, font=dict(size=13, color="#0f172a", family="Inter,sans-serif"), x=0, pad=dict(l=0, t=0)),
        plot_bgcolor=_TRANS, paper_bgcolor=_TRANS, font=_FONT, height=height,
        margin=dict(l=16, r=16, t=36, b=24),
        legend=dict(orientation="h", yanchor="bottom", y=-0.28, xanchor="center", x=0.5, font=dict(size=11)),
    )


def sentiment_donut(df: pd.DataFrame):
    counts  = df['sentiment'].value_counts().reset_index()
    counts.columns = ['sentiment', 'count']
    total   = counts['count'].sum()
    colors  = [SENTIMENT_COLORS.get(s, "#94a3b8") for s in counts['sentiment']]
    labels  = [f"{s.capitalize()}<br>{c} reviews" for s, c in zip(counts['sentiment'], counts['count'])]
    fig = go.Figure(go.Pie(
        labels=counts['sentiment'].str.capitalize(),
        values=counts['count'],
        hole=0.60,
        marker=dict(colors=colors, line=dict(color="#fff", width=3)),
        textinfo="percent",
        textfont=dict(size=12, color="#fff"),
        hovertemplate="%{label}: %{value} reviews (%{percent})<extra></extra>",
        customdata=counts['count'],
    ))
    fig.add_annotation(text=f"<b>{total}</b><br><span style='font-size:10px'>Total Reviews</span>",
                       x=0.5, y=0.5, showarrow=False, font=dict(size=15, color="#0f172a"))
    fig.update_layout(**_base("", 300))
    return fig


def rating_bar(df: pd.DataFrame):
    dist  = df.groupby('rating').size().reset_index(name='count')
    dist['rating_str'] = dist['rating'].astype(str) + " Stars"
    clrs  = {1:"#ef4444", 2:"#f97316", 3:"#f59e0b", 4:"#84cc16", 5:"#22c55e"}
    colors = [clrs.get(r, "#3b82f6") for r in dist['rating']]
    fig = go.Figure(go.Bar(
        x=dist['rating_str'], y=dist['count'], text=dist['count'],
        textposition='outside', marker_color=colors, marker_line_width=0,
    ))
    fig.update_xaxes(title_text="Star Rating", gridcolor=_GRID, zeroline=False)
    fig.update_yaxes(title_text="Reviews", gridcolor=_GRID, zeroline=False, showgrid=True)
    fig.update_layout(**_base("", 300), showlegend=False)
    return fig


def brand_sentiment_bar(df: pd.DataFrame):
    summary   = df.groupby(['brand', 'sentiment']).size().reset_index(name='count')
    color_map = {"positive": SENTIMENT_COLORS["positive"], "negative": SENTIMENT_COLORS["negative"], "mixed": SENTIMENT_COLORS["mixed"]}
    fig = px.bar(summary, x='brand', y='count', color='sentiment', barmode='stack',
                 color_discrete_map=color_map, text='count')
    fig.update_traces(textposition='inside', textfont_size=10, marker_line_width=0)
    fig.update_xaxes(title_text="", tickangle=-20, gridcolor=_GRID)
    fig.update_yaxes(title_text="Review Count", gridcolor=_GRID, zeroline=False)
    fig.update_layout(**_base("", 340))
    return fig


def avg_rating_brand(df: pd.DataFrame):
    avg = df.groupby('brand')['rating'].mean().reset_index()
    avg.columns = ['brand', 'avg_rating']
    avg = avg.sort_values('avg_rating', ascending=False)
    colors = []
    for v in avg['avg_rating']:
        if v >= 4.0:   colors.append("#22c55e")
        elif v >= 3.0: colors.append("#f59e0b")
        else:          colors.append("#ef4444")
    fig = go.Figure(go.Bar(
        x=avg['brand'], y=avg['avg_rating'],
        text=avg['avg_rating'].round(2), textposition='outside',
        marker_color=colors, marker_line_width=0,
    ))
    fig.update_xaxes(title_text="", tickangle=-20, gridcolor=_GRID)
    fig.update_yaxes(title_text="Avg Rating", gridcolor=_GRID, zeroline=False, range=[0, 5.5])
    fig.update_layout(**_base("", 320), showlegend=False)
    return fig


def complaint_bar(df: pd.DataFrame):
    neg = df[df['sentiment'] == 'negative']
    if neg.empty:
        return None
    top = neg.groupby('category').size().reset_index(name='count').sort_values('count', ascending=False).head(8)
    top['label'] = top['category'].map(lambda x: CATEGORY_LABELS.get(x, x.replace('_', ' ').title()))
    fig = px.bar(top.sort_values('count'), x='count', y='label', orientation='h',
                 color_discrete_sequence=["#ef4444"], text='count')
    fig.update_traces(textposition='outside', marker_line_width=0)
    fig.update_xaxes(title_text="Mentions", gridcolor=_GRID, zeroline=False)
    fig.update_yaxes(title_text="")
    fig.update_layout(**_base("", 300), showlegend=False)
    return fig


def keyword_treemap(word_freq: dict):
    if not word_freq:
        return None
    labels = list(word_freq.keys())
    values = list(word_freq.values())
    fig = go.Figure(go.Treemap(
        labels=labels, parents=[""]*len(labels), values=values,
        marker=dict(colorscale=[[0,"#dbeafe"],[0.5,"#3b82f6"],[1,"#1d4ed8"]], colors=values),
        textfont=dict(size=13, family="Inter,sans-serif"),
        hovertemplate="<b>%{label}</b><br>Mentions: %{value}<extra></extra>",
    ))
    fig.update_layout(**_base("", 260))
    return fig


def competitor_radar(comp_df: pd.DataFrame):
    cats   = ['Avg Rating', 'Positive %', 'Sentiment Score']
    colors = ["#3b82f6","#22c55e","#f59e0b","#ef4444","#8b5cf6","#ec4899"]
    fig    = go.Figure()
    for i, (_, row) in enumerate(comp_df.iterrows()):
        vals = [row['avg_rating']*20, row['positive_pct'], row['sentiment_score']]
        vals += [vals[0]]
        c     = colors[i % len(colors)]
        r, g, b = int(c[1:3],16), int(c[3:5],16), int(c[5:7],16)
        fig.add_trace(go.Scatterpolar(
            r=vals, theta=cats+[cats[0]], fill='toself',
            fillcolor=f"rgba({r},{g},{b},0.12)",
            line=dict(color=c, width=2), name=row['brand'],
            hovertemplate=f"<b>{row['brand']}</b><br>%{{theta}}: %{{r:.1f}}<extra></extra>",
        ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0,100], tickfont=dict(size=9), gridcolor=_GRID),
                   angularaxis=dict(tickfont=dict(size=11))),
        **_base("", 360),
    )
    return fig


def timeline_sentiment(df: pd.DataFrame):
    if 'date' not in df.columns:
        return None
    df2 = df.copy()
    df2['month'] = df2['date'].dt.to_period('M').astype(str)
    monthly = df2.groupby(['month','sentiment']).size().reset_index(name='count')
    color_map = {"positive":SENTIMENT_COLORS["positive"],"negative":SENTIMENT_COLORS["negative"],"mixed":SENTIMENT_COLORS["mixed"]}
    fig = px.line(monthly, x='month', y='count', color='sentiment', color_discrete_map=color_map, markers=True)
    fig.update_xaxes(title_text="", gridcolor=_GRID, tickangle=-20)
    fig.update_yaxes(title_text="Reviews", gridcolor=_GRID, zeroline=False)
    fig.update_layout(**_base("", 280))
    return fig
