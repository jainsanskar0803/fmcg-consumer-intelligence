import os
from dotenv import load_dotenv
load_dotenv()

# ── AI Provider ─────────────────────────────────────────────────────────────
# Supported: "gemini" or "groq"
AI_PROVIDER    = os.getenv("AI_PROVIDER", "gemini")

# Gemini — get free key at https://aistudio.google.com
GEMINI_API_KEY  = os.getenv("GEMINI_API_KEY", "")
# Gemini model options: "gemini-2.5-flash-preview-04-17", "gemini-2.0-flash"
GEMINI_MODEL    = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

# Groq — get free key at https://console.groq.com
GROQ_API_KEY    = os.getenv("GROQ_API_KEY", "")
# Groq model options: "llama3-8b-8192", "mixtral-8x7b-32768", "llama3-70b-8192"
GROQ_MODEL      = os.getenv("GROQ_MODEL", "llama3-8b-8192")

# ── MongoDB ──────────────────────────────────────────────────────────────────
# Strip surrounding quotes that some .env parsers leave in
MONGO_URI      = os.getenv("MONGO_URI", "mongodb://localhost:27017/").strip('"').strip("\'")
MONGO_DB_NAME  = os.getenv("MONGO_DB_NAME", "fmcg_intelligence")

# ── ChromaDB ─────────────────────────────────────────────────────────────────
CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")

# ── Brands ───────────────────────────────────────────────────────────────────
EMAMI_BRANDS      = ["Navratna Oil", "Kesh King Oil", "BoroPlus"]
COMPETITOR_BRANDS = ["Dabur Amla", "Mamaearth Onion Oil", "Himalaya Hair Oil"]
ALL_BRANDS        = EMAMI_BRANDS + COMPETITOR_BRANDS

SENTIMENT_COLORS = {"positive": "#22c55e", "negative": "#ef4444", "mixed": "#f59e0b"}

CATEGORY_LABELS = {
    "cooling": "Cooling Effect", "fragrance": "Smell / Fragrance",
    "packaging": "Packaging", "hair_care": "Hair Care",
    "pricing": "Price", "texture": "Texture / Feel",
    "hair_growth": "Hair Growth", "brand_trust": "Brand Trust",
    "ingredients": "Ingredients", "moisturizing": "Moisturizing",
    "healing": "Healing", "value": "Value for Money",
    "safety": "Safety", "wellness": "Wellness",
    "availability": "Availability", "product_quality": "Product Quality",
    "customer_service": "Customer Service", "skin_type": "Skin Type",
    "brand_relevance": "Brand Relevance", "product_range": "Product Range",
}
