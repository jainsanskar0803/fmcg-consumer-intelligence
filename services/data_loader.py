import pandas as pd
import streamlit as st
import os
import io
from pathlib import Path


DATA_FILE = Path(__file__).parent.parent / "data" / "reviews_dataset.csv"


@st.cache_data(ttl=300)
def load_demo_data() -> pd.DataFrame:
    """Load built-in demo dataset."""
    df = pd.read_csv(DATA_FILE)
    df['date'] = pd.to_datetime(df['date'])
    df['rating'] = df['rating'].astype(int)
    df['review_text'] = df['review_text'].astype(str)
    return df


def load_uploaded_csv(uploaded_file) -> pd.DataFrame:
    """Parse user-uploaded CSV file."""
    try:
        df = pd.read_csv(uploaded_file)
        required_cols = {'review_text', 'rating', 'sentiment'}
        missing = required_cols - set(df.columns)
        if missing:
            st.warning(f"Missing columns: {missing}. Using available data.")
        # Fill optional columns
        if 'brand' not in df.columns:
            df['brand'] = 'Unknown'
        if 'product' not in df.columns:
            df['product'] = 'Unknown'
        if 'category' not in df.columns:
            df['category'] = 'general'
        if 'date' not in df.columns:
            df['date'] = pd.Timestamp.now()
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df['rating'] = pd.to_numeric(df['rating'], errors='coerce').fillna(3).astype(int)
        return df
    except Exception as e:
        st.error(f"Error reading CSV: {str(e)}")
        return pd.DataFrame()


def load_txt_file(uploaded_file) -> pd.DataFrame:
    """Parse plain text file — one review per line."""
    try:
        content = uploaded_file.read().decode('utf-8')
        lines = [line.strip() for line in content.splitlines() if line.strip()]
        df = pd.DataFrame({
            'review_text': lines,
            'brand': 'Uploaded',
            'product': 'Unknown',
            'rating': 3,
            'sentiment': 'mixed',
            'category': 'general',
            'date': pd.Timestamp.now(),
        })
        return df
    except Exception as e:
        st.error(f"Error reading TXT file: {str(e)}")
        return pd.DataFrame()


def filter_dataframe(
    df: pd.DataFrame,
    brands: list = None,
    sentiments: list = None,
    categories: list = None,
    rating_range: tuple = (1, 5),
) -> pd.DataFrame:
    filtered = df.copy()
    if brands:
        filtered = filtered[filtered['brand'].isin(brands)]
    if sentiments:
        filtered = filtered[filtered['sentiment'].isin(sentiments)]
    if categories:
        filtered = filtered[filtered['category'].isin(categories)]
    filtered = filtered[
        (filtered['rating'] >= rating_range[0]) &
        (filtered['rating'] <= rating_range[1])
    ]
    return filtered


def get_brand_subset(df: pd.DataFrame, brand: str) -> pd.DataFrame:
    return df[df['brand'] == brand].copy()
