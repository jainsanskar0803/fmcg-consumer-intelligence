"""
MongoDB Atlas integration — gracefully degrades if not available.
"""

from datetime import datetime
from utils.config import MONGO_URI, MONGO_DB_NAME

_client = None
_db     = None
_failed = False   # only skip retries after a confirmed failure


def get_db():
    global _client, _db, _failed
    if _db is not None:
        return _db
    if _failed:
        return None
    try:
        from pymongo import MongoClient
        # Atlas needs 8-10s; local is instant
        _client = MongoClient(
            MONGO_URI,
            serverSelectionTimeoutMS=10000,
            connectTimeoutMS=10000,
            socketTimeoutMS=10000,
            tls=True,               # always required for Atlas
            tlsAllowInvalidCertificates=False,
        )
        _client.admin.command("ping")   # lighter than server_info()
        _db = _client[MONGO_DB_NAME]
        return _db
    except Exception as e:
        _failed = True
        return None


def reset_connection():
    """Call this to force a reconnect attempt (e.g. after config change)."""
    global _client, _db, _failed
    _client = None
    _db     = None
    _failed = False


def save_upload_metadata(filename: str, file_type: str, row_count: int, brands: list):
    db = get_db()
    if db is None:
        return False
    try:
        db.uploads.insert_one({
            "filename":    filename,
            "file_type":   file_type,
            "row_count":   row_count,
            "brands":      brands,
            "uploaded_at": datetime.utcnow(),
        })
        return True
    except Exception:
        return False


def save_query_history(question: str, answer: str, dataset: str):
    db = get_db()
    if db is None:
        return False
    try:
        db.query_history.insert_one({
            "question": question,
            "answer":   answer[:500],
            "dataset":  dataset,
            "asked_at": datetime.utcnow(),
        })
        return True
    except Exception:
        return False


def get_recent_queries(limit: int = 10) -> list:
    db = get_db()
    if db is None:
        return []
    try:
        return list(
            db.query_history.find({}, {"_id": 0})
            .sort("asked_at", -1)
            .limit(limit)
        )
    except Exception:
        return []


def get_upload_history(limit: int = 20) -> list:
    db = get_db()
    if db is None:
        return []
    try:
        return list(
            db.uploads.find({}, {"_id": 0})
            .sort("uploaded_at", -1)
            .limit(limit)
        )
    except Exception:
        return []


def is_mongodb_connected() -> bool:
    return get_db() is not None
