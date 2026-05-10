"""
RAG pipeline: chunking, embedding, ChromaDB storage and retrieval.
"""

import streamlit as st


@st.cache_resource(show_spinner=False)
def get_chroma_client():
    try:
        import chromadb
        return chromadb.Client()
    except Exception:
        return None


@st.cache_resource(show_spinner=False)
def get_embedding_function():
    try:
        from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
        return SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
    except Exception:
        return None


def build_rag_collection(df, collection_name="fmcg_reviews"):
    """Build ChromaDB collection. Called explicitly — not cached."""
    client = get_chroma_client()
    emb_fn = get_embedding_function()
    if client is None or emb_fn is None:
        return False
    try:
        try:
            client.delete_collection(collection_name)
        except Exception:
            pass
        collection = client.create_collection(name=collection_name, embedding_function=emb_fn)
        docs, ids, metas = [], [], []
        for i, (_, row) in enumerate(df.iterrows()):
            text = (
                f"Brand: {row['brand']}. Sentiment: {row['sentiment']}. "
                f"Category: {row.get('category','')}. Rating: {row['rating']}. "
                f"Review: {row['review_text']}"
            )
            docs.append(text)
            ids.append(f"doc_{i}")
            metas.append({
                "brand": str(row['brand']),
                "sentiment": str(row['sentiment']),
                "category": str(row.get('category', '')),
                "rating": int(row['rating']),
            })
        for start in range(0, len(docs), 50):
            end = min(start + 50, len(docs))
            collection.add(documents=docs[start:end], ids=ids[start:end], metadatas=metas[start:end])
        return True
    except Exception:
        return False


def retrieve_context(query, collection_name="fmcg_reviews", n=6):
    client = get_chroma_client()
    emb_fn = get_embedding_function()
    if client is None or emb_fn is None:
        return ""
    try:
        collection = client.get_collection(name=collection_name, embedding_function=emb_fn)
        results = collection.query(query_texts=[query], n_results=min(n, collection.count()))
        return "\n".join(results.get('documents', [[]])[0])
    except Exception:
        return ""
