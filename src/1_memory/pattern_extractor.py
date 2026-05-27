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
# ---------------------- DI ---------------------- DI ---------------------- DI ---------------------- DI ----------------------

# Interaction Counter
def get_interaction_count() -> int:
    conn = sqlite3.connect(DB_PATH)
    count = conn.execute(
        "SELECT COUNT(*) FROM messages WHERE role = 'user'"
    ).fetchone()[0]
    conn.close()
    return count
 
def should_extract() -> bool:
    return get_interaction_count() % TRIGGER_EVERY == 0
# ---------------------- DI ---------------------- DI ---------------------- DI ---------------------- DI ----------------------

#Data Loaders
def load_conversation_history() -> str:
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute(
        "SELECT role, content, timestamp FROM messages ORDER BY id"
    ).fetchall()
    conn.close()
    if not rows:
        return ""
    lines = [f"[{r[2][:16]}] {r[0].upper()}: {r[1]}" for r in rows]
    return "\n".join(lines)
 
def load_unprocessed_journals() -> list[dict]:
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute(
        "SELECT id, content, added_at FROM journal_entries WHERE processed = 0"
    ).fetchall()
    conn.close()
    return [{"id": r[0], "content": r[1], "added_at": r[2]} for r in rows]
 
def mark_journals_processed(ids: list[int]):
    if not ids:
        return
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        f"UPDATE journal_entries SET processed = 1 WHERE id IN ({','.join('?'*len(ids))})",
        ids
    )
    conn.commit()
    conn.close()
 
def add_journal_entry(content: str):
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO journal_entries (content, added_at) VALUES (?, ?)",
        (content, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()
    print("\n Journal entry saved.\n")

# ---------------------- DI ---------------------- DI ---------------------- DI ---------------------- DI ----------------------

#LLM Extraction
EXTRACTION_PROMPT = """You are a cognitive analyst. Analyse the following text - which may include conversation history, journal entries, or personal notes - and extract structured patterns about how this person thinks.
 
Return ONLY a valid JSON object with this exact structure (no preamble, no markdown):
 
{{
  "dominant_reasoning_styles": ["list of observed styles, e.g. deductive, intuitive, analogical"],
  "cognitive_biases": [
    {{"name": "bias name", "evidence": "short quote or paraphrase from text", "frequency": "low|medium|high"}}
  ],
  "mental_models": ["frameworks or lenses the person naturally reaches for"],
  "blind_spots": ["topics, question types, or perspectives consistently avoided or missed"],
  "growth_signals": ["areas where thinking is visibly developing or improving"],
  "summary": "2-3 sentence synthesis of this person's overall cognitive profile based on this data"
}}
 
Be specific. Base every field on actual evidence from the text.
Do not invent patterns that are not present.
If a field has no evidence, return an empty list.
 
TEXT TO ANALYSE:
{text}"""
 
client = Anthropic()
 
def extract_patterns(text: str, source: str) -> dict | None:
    if not text.strip():
        print(f"  No {source} data to analyse.")
        return None
 
    print(f"\n Extracting patterns from {source}...")
 
    response = client.messages.create(
        model      = MODEL,
        max_tokens = 1024,
        messages   = [{
            "role"   : "user",
            "content": EXTRACTION_PROMPT.format(text=text)
        }]
    )
 
    raw = response.content[0].text.strip()
 
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        # Strip possible markdown fences
        raw = raw.replace("```json", "").replace("```", "").strip()
        parsed = json.loads(raw)
 
    return parsed