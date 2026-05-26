import os
import json
import sqlite3
from datetime import datetime
from anthropic import Anthropic
# ---------------------- DI ---------------------- DI ---------------------- DI ---------------------- DI ----------------------

# Config
DB_PATH       = "memory.db"
PATTERNS_JSON = "patterns.json"
MODEL         = "claude-opus-4-6"
TRIGGER_EVERY = 5   # run extraction after every N user interactions

# ---------------------- DI ---------------------- DI ---------------------- DI ---------------------- DI ----------------------

# Database Setup
def init_patterns_table():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS patterns (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            extracted_at    TEXT    NOT NULL,
            source          TEXT    NOT NULL,  -- 'conversation' | 'journal'
            dominant_styles TEXT,              -- JSON list
            cognitive_biases TEXT,             -- JSON list
            mental_models   TEXT,              -- JSON list
            blind_spots     TEXT,              -- JSON list
            growth_signals  TEXT,              -- JSON list
            raw_json        TEXT    NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS journal_entries (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            content     TEXT    NOT NULL,
            added_at    TEXT    NOT NULL,
            processed   INTEGER DEFAULT 0      -- 0 = not yet extracted
        )
    """)
    conn.commit()
    conn.close()