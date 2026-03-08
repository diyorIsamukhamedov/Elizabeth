import os
import sqlite3
from datetime import datetime
#Install the official Anthropic Python SDK
from anthropic import Anthropic

# ---------------------- DI ---------------------- DI ---------------------- DI ---------------------- DI ----------------------
# Config
DB_PATH = "elizabeth.db"
MODEL = "claude-opus-4-6"

SYSTEM_PROMPT = """You are Elizabeth - an adaptive personal intelligence system.

I'm your creator and you're my creature - "Elizabeth". My name's DIYOR.

Your role is not just to answer questions. Your role is to:
1. Understand HOW the user thinks, not just WHAT they ask
2. Notice patterns in their reasoning across conversations
3. Gently challenge assumptions and cognitive blind spots
4. Help them think more clearly over time

You have access to the full conversation history. Use it.
Pay attention to recurring themes, contradictions, and growth.
Be direct. Be honest. Be a thinking partner, not a yes-machine."""
# ---------------------- DI ---------------------- DI ---------------------- DI ---------------------- DI ----------------------

# ---------------------- DI ---------------------- DI ---------------------- DI ---------------------- DI ----------------------
# Database
def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp TEXT NOT NULL         
        )
    """)

    conn.commit()
    conn.close()

def save_message(role: str, content: str):
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO messages (role, content, timestamp) VALUES (?, ?, ?)",
        (role, content, datetime.now().isoformat())
    )

    conn.commit()
    conn.close()

def load_history() -> list[dict]:
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute(
        "SELECT role, content FROM messages ORDER BY id"
    ).fetchall()
    conn.close()
    return [{"role": row[0], "content": row[1]} for row in rows]

def get_stats() -> dict:
    conn = sqlite3.connect(DB_PATH)
    total      = conn.execute("SELECT COUNT(*) FROM messages").fetchone()[0]
    user_count = conn.execute("SELECT COUNT(*) FROM messages WHERE role='user'").fetchone()[0]
    first_date = conn.execute("SELECT timestamp FROM messages ORDER BY id LIMIT 1").fetchone()
    conn.close()
    return {
        "total_messages" : total,
        "interactions"   : user_count,
        "since"          : first_date[0][:10] if first_date else "today"
    }
# ---------------------- DI ---------------------- DI ---------------------- DI ---------------------- DI ----------------------

# ---------------------- DI ---------------------- DI ---------------------- DI ---------------------- DI ----------------------
#LLM
def get_response(history: list[dict]) -> str:
    response = client.messages.create(
        model      = MODEL,
        max_tokens = 1024,
        system     = SYSTEM_PROMPT,
        messages   = history
    )

    return response.content[0].text
# ---------------------- DI ---------------------- DI ---------------------- DI ---------------------- DI ----------------------

# ---------------------- DI ---------------------- DI ---------------------- DI ---------------------- DI ----------------------
#CLI