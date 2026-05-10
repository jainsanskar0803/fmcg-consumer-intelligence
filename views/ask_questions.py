import streamlit as st
import pandas as pd
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.llm_service import get_ai_response, build_insight_prompt
from services.mongodb_service import save_query_history
from rag.embeddings import build_rag_collection, retrieve_context
from utils.helpers import reviews_to_context_text
from utils.config import ALL_BRANDS, GEMINI_API_KEY, GROQ_API_KEY

_SAMPLE_QUESTIONS = [
    "Why are customers unhappy with Navratna Oil?",
    "Compare primary and competitor brands",
    "What packaging problems are being reported?",
    "Summarize Kesh King feedback in 3 points",
    "Which brand has the happiest customers?",
    "What improvements are customers asking for?",
    "How does Mamaearth compare on fragrance?",
    "What are the top 3 reasons for bad reviews?",
]


def _run_query(question: str, df: pd.DataFrame, brand_scope: str):
    filtered = df.copy() if brand_scope == "All brands" else df[df["brand"] == brand_scope].copy()
    if st.session_state.get("rag_built"):
        context = retrieve_context(question) or reviews_to_context_text(filtered, 60)
    else:
        context = reviews_to_context_text(filtered, 60)
    brand_f = brand_scope if brand_scope != "All brands" else "all"
    prompt  = build_insight_prompt(question, context, brand_f)
    answer  = get_ai_response(prompt, context, question)
    st.session_state.chat_history.append({"question": question, "answer": answer, "brand": brand_scope})
    save_query_history(question, answer, st.session_state.get("data_source", "demo"))


def render_ask_questions(df: pd.DataFrame):
    st.markdown('<div class="page-title">Ask a Business Question</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Type any question about customer reviews — AI reads the data and answers instantly</div>', unsafe_allow_html=True)

    if df.empty:
        st.warning("No data loaded.")
        return

    api_ready = bool(GEMINI_API_KEY or GROQ_API_KEY)
    rag_built = st.session_state.get("rag_built", False)

    # Status / RAG build
    s1, s2, _ = st.columns([1.2, 1.8, 2])
    with s1:
        if rag_built:
            st.success("✅ Search index ready")
        else:
            if st.button("⚡ Build Search Index", key="build_rag"):
                with st.spinner("Indexing reviews…"):
                    ok = build_rag_collection(df)
                    st.session_state.rag_built = ok
                    st.rerun()
    with s2:
        status_txt = "🤖 AI ready" if api_ready else "⚠️ Add API key to .env"
        st.markdown(f"<div style='padding:10px 0;font-size:0.8rem;color:#64748b;'>{status_txt} &nbsp;·&nbsp; {len(df)} reviews</div>",
                    unsafe_allow_html=True)

    st.markdown("<div style='margin-top:14px'></div>", unsafe_allow_html=True)
    brand_scope = st.selectbox("Filter to one brand (optional)", ["All brands"] + ALL_BRANDS, key="qa_scope")
    st.markdown("<div style='margin-top:18px'></div>", unsafe_allow_html=True)

    # Quick questions
    st.markdown("""<div class="chart-card">
        <div class="chart-title">Quick Questions</div>
        <div class="chart-subtitle">Click any to get an instant AI answer</div>""",
        unsafe_allow_html=True)
    cols = st.columns(4)
    for i, q in enumerate(_SAMPLE_QUESTIONS):
        with cols[i % 4]:
            if st.button(q, key=f"sq_{i}", use_container_width=True):
                with st.spinner("Analysing reviews…"):
                    _run_query(q, df, brand_scope)
                st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    # Manual input
    st.markdown("""<div class="chart-card">
        <div class="chart-title">Ask Your Own Question</div>
        <div class="chart-subtitle">Ask anything about any brand, product, or customer trend</div>""",
        unsafe_allow_html=True)
    question = st.text_area(
        "question",
        placeholder="e.g.  What are customers saying about Navratna Oil packaging?",
        height=88, label_visibility="collapsed", key="manual_q",
    )
    st.markdown("<div style='margin-top:10px'></div>", unsafe_allow_html=True)
    if st.button("🔍  Get Answer", key="ask_btn"):
        if question.strip():
            with st.spinner("Reading reviews and generating answer…"):
                _run_query(question.strip(), df, brand_scope)
            st.rerun()
        else:
            st.warning("Please type a question first.")
    st.markdown("</div>", unsafe_allow_html=True)

    # Chat history
    if st.session_state.get("chat_history"):
        st.markdown("""<div class="chart-card">
            <div class="chart-title">Answers</div>
            <div class="chart-subtitle">All questions this session — newest first</div>""",
            unsafe_allow_html=True)
        for entry in reversed(st.session_state.chat_history):
            st.markdown(f"""
            <div style="background:#eff6ff;border:1px solid #bfdbfe;border-radius:8px;
                        padding:12px 16px;margin-bottom:10px;font-size:0.85rem;color:#1e3a8a;">
                <div style="font-size:0.66rem;font-weight:700;text-transform:uppercase;
                            letter-spacing:0.05em;color:#3b82f6;margin-bottom:5px;">
                    Question · {entry.get('brand','All brands')}
                </div>
                {entry['question']}
            </div>
            <div class="insight-box" style="margin-bottom:20px;">
                <div style="font-size:0.66rem;font-weight:700;text-transform:uppercase;
                            letter-spacing:0.05em;color:#3b82f6;margin-bottom:8px;">Answer</div>
                {entry['answer'].replace(chr(10), '<br>')}
            </div>""", unsafe_allow_html=True)
        if st.button("🗑  Clear answers", key="clear_chat"):
            st.session_state.chat_history = []
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
