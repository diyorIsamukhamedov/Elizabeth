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