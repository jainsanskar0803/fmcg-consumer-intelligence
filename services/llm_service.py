import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.config import AI_PROVIDER, GEMINI_API_KEY, GEMINI_MODEL, GROQ_API_KEY, GROQ_MODEL

# ── Gemini ────────────────────────────────────────────────────────────────────
def _gemini_response(prompt: str) -> str:
    try:
        import google.generativeai as genai
        genai.configure(api_key=GEMINI_API_KEY)
        # Try configured model first, then fallbacks
        models_to_try = list(dict.fromkeys([
            GEMINI_MODEL,
            "gemini-2.0-flash",
            "gemini-2.5-flash-preview-04-17",
            "gemini-1.5-flash",
            "gemini-1.5-flash-latest",
        ]))
        last_err = ""
        for m in models_to_try:
            try:
                resp = genai.GenerativeModel(m).generate_content(prompt)
                return resp.text.strip()
            except Exception as e:
                last_err = str(e)
                if "quota" in str(e).lower() or "billing" in str(e).lower():
                    break
                continue
        return f"Gemini error: {last_err}"
    except Exception as e:
        return f"Gemini setup error: {str(e)}"


# ── Groq ──────────────────────────────────────────────────────────────────────
def _groq_response(prompt: str) -> str:
    try:
        from groq import Groq
        client = Groq(api_key=GROQ_API_KEY)
        resp   = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": "You are a consumer insights analyst. Give clear, concise, data-driven answers in plain English."},
                {"role": "user",   "content": prompt},
            ],
            max_tokens=600,
            temperature=0.4,
        )
        return resp.choices[0].message.content.strip()
    except ImportError:
        return "Groq SDK not installed. Run: pip install groq"
    except Exception as e:
        return f"Groq error: {str(e)}"


# ── Demo fallback ─────────────────────────────────────────────────────────────
def _demo_response() -> str:
    return (
        "**No API key configured.**\n\n"
        "Add one of these to your `.env` file:\n\n"
        "**Gemini** (free): Get key at https://aistudio.google.com\n"
        "`GEMINI_API_KEY=your-key`\n\n"
        "**Groq** (free): Get key at https://console.groq.com\n"
        "`GROQ_API_KEY=your-key`\n\n"
        "---\n**Sample answer:**\n\n"
        "Navratna Oil has strong positive reviews around cooling effect (40%+ of 5-star reviews). "
        "Main complaint is packaging leakage (15% of negatives). Mamaearth scores better on texture.\n\n"
        "**Recommendation:** Fix the bottle cap seal and test a lighter fragrance variant for urban buyers."
    )


# ── Main entry ────────────────────────────────────────────────────────────────
def get_ai_response(prompt: str, context: str = "", question: str = "") -> str:
    if context and question:
        full_prompt = (
            f"Customer review data:\n\n{context}\n\n"
            f"Question: {question}\n\n"
            "Answer in 150-200 words. Simple language. "
            "Mention specific brands and numbers. End with one clear recommendation."
        )
    else:
        full_prompt = prompt

    if AI_PROVIDER == "groq" and GROQ_API_KEY:
        return _groq_response(full_prompt)
    elif AI_PROVIDER == "gemini" and GEMINI_API_KEY:
        return _gemini_response(full_prompt)
    elif GEMINI_API_KEY:
        return _gemini_response(full_prompt)
    elif GROQ_API_KEY:
        return _groq_response(full_prompt)
    else:
        return _demo_response()


def build_insight_prompt(question: str, context: str, brand_filter: str = "all") -> str:
    brand_note = f"Focus only on {brand_filter}." if brand_filter != "all" else ""
    return (
        f"Customer review data:\n\n{context}\n\n"
        f"Question: {question}\n{brand_note}\n\n"
        "Answer clearly in under 200 words. Mention specific product names and numbers. "
        "End with one practical recommendation."
    )


def generate_executive_summary(context: str, brands: list) -> str:
    prompt = (
        f"Write an executive summary for these brands: {', '.join(brands)}.\n\n"
        f"Customer review data:\n{context}\n\n"
        "Structure:\n"
        "1. Overall picture (2 sentences)\n"
        "2. What customers like most (2-3 points)\n"
        "3. Top complaints to fix (2-3 points)\n"
        "4. Competitor comparison (2 sentences)\n"
        "5. Three immediate actions\n\n"
        "Plain English. No jargon. Under 300 words."
    )
    return get_ai_response(prompt)


def get_active_provider_name() -> str:
    """Returns display name for UI — never shows Groq/Gemini brand."""
    if AI_PROVIDER == "groq" and GROQ_API_KEY:
        return "AI Active"
    elif GEMINI_API_KEY or GROQ_API_KEY:
        return "AI Active"
    return "No API Key"
