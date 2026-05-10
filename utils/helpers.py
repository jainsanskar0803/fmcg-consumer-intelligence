import pandas as pd
import re
from datetime import datetime


def clean_review_text(text: str) -> str:
    """Basic text cleaning while preserving Hinglish."""
    if not isinstance(text, str):
        return ""
    text = text.strip()
    text = re.sub(r'\s+', ' ', text)
    return text


def format_large_number(n: int) -> str:
    if n >= 1000:
        return f"{n/1000:.1f}K"
    return str(n)


def compute_sentiment_score(df: pd.DataFrame) -> float:
    """Returns a 0-100 sentiment health score."""
    if df.empty:
        return 0.0
    counts = df['sentiment'].value_counts()
    total = len(df)
    pos = counts.get('positive', 0)
    neg = counts.get('negative', 0)
    mixed = counts.get('mixed', 0)
    score = (pos * 1.0 + mixed * 0.5 - neg * 0.5) / total * 100
    return round(max(0, min(100, score)), 1)


def get_top_complaints(df: pd.DataFrame, n: int = 5) -> pd.DataFrame:
    """Returns top negative feedback categories."""
    neg_df = df[df['sentiment'] == 'negative']
    if neg_df.empty:
        return pd.DataFrame()
    return (
        neg_df.groupby('category')
        .size()
        .reset_index(name='count')
        .sort_values('count', ascending=False)
        .head(n)
    )


def get_rating_distribution(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby('rating')
        .size()
        .reset_index(name='count')
        .sort_values('rating')
    )


def compute_nps_proxy(df: pd.DataFrame) -> float:
    """Net Promoter Score proxy based on ratings."""
    if df.empty:
        return 0.0
    promoters = len(df[df['rating'] >= 4])
    detractors = len(df[df['rating'] <= 2])
    total = len(df)
    if total == 0:
        return 0.0
    return round((promoters - detractors) / total * 100, 1)


def extract_keywords_frequency(df: pd.DataFrame, top_n: int = 15) -> dict:
    """Simple keyword frequency from review text."""
    stop_words = {
        'the', 'a', 'an', 'is', 'it', 'in', 'on', 'at', 'to', 'for',
        'of', 'and', 'or', 'but', 'not', 'with', 'this', 'that', 'are',
        'was', 'be', 'as', 'my', 'i', 'me', 'very', 'so', 'has', 'have',
        'had', 'by', 'from', 'its', 'been', 'too', 'after', 'also',
        'just', 'than', 'into', 'use', 'used', 'using', 'get', 'got',
        'more', 'much', 'can', 'will', 'would', 'could', 'all', 'no',
        'do', 'did', 'which', 'when', 'who', 'how', 'what', 'only',
        'now', 'like', 'feels', 'feel', 'even', 'still', 'never', 'any',
        'good', 'great', 'best', 'bad', 'really', 'well',
    }
    word_freq = {}
    for text in df['review_text'].dropna():
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        for word in words:
            if word not in stop_words:
                word_freq[word] = word_freq.get(word, 0) + 1

    sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
    return dict(sorted_words[:top_n])


def build_competitor_comparison(df: pd.DataFrame) -> pd.DataFrame:
    """Builds brand-level summary for competitor comparison."""
    summary = []
    for brand in df['brand'].unique():
        bdf = df[df['brand'] == brand]
        sentiment_counts = bdf['sentiment'].value_counts()
        total = len(bdf)
        summary.append({
            'brand': brand,
            'total_reviews': total,
            'avg_rating': round(bdf['rating'].mean(), 2),
            'positive_pct': round(sentiment_counts.get('positive', 0) / total * 100, 1),
            'negative_pct': round(sentiment_counts.get('negative', 0) / total * 100, 1),
            'mixed_pct': round(sentiment_counts.get('mixed', 0) / total * 100, 1),
            'sentiment_score': compute_sentiment_score(bdf),
            'nps_proxy': compute_nps_proxy(bdf),
        })
    return pd.DataFrame(summary).sort_values('sentiment_score', ascending=False)


def reviews_to_context_text(df: pd.DataFrame, max_rows: int = 80) -> str:
    """Converts dataframe to text context for LLM."""
    sample = df.sample(min(max_rows, len(df)), random_state=42)
    lines = []
    for _, row in sample.iterrows():
        lines.append(
            f"[{row['brand']} | {row['sentiment']} | {row['category']} | Rating: {row['rating']}] "
            f"{row['review_text']}"
        )
    return "\n".join(lines)
