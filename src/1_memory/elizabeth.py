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
def print_banner():
    stats = get_stats()
    print("\n" + "─" * 55)
    print("  🧠  E L I Z A B E T H")
    print("  Adaptive Personal Intelligence System")
    print("─" * 55)
    if stats["total_messages"] > 0:
        print(f"  Memory: {stats['interactions']} interactions since {stats['since']}")
    else:
        print("  Memory: fresh start — no history yet")
    print("─" * 55)
    print("  Commands:  'quit' to exit  |  'clear' to reset memory")
    print("─" * 55 + "\n")
 
def clear_memory():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("DELETE FROM messages")
    conn.commit()
    conn.close()
    print("\n  Memory cleared.\n")
# ---------------------- DI ---------------------- DI ---------------------- DI ---------------------- DI ----------------------
def main():
    init_db()
    print_banner()
 
    while True:
        try:
            user_input = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\n  Goodbye.\n")
            break
 
        if not user_input:
            continue
 
        if user_input.lower() == "quit":
            print("\n  Goodbye.\n")
            break
 
        if user_input.lower() == "clear":
            clear_memory()
            continue
 
        # Save user message
        save_message("user", user_input)
 
        # Load full history and get response
        history  = load_history()
        response = get_response(history)
 
        # Save and display response
        save_message("assistant", response)
        print(f"\nElizabeth: {response}\n")
 
if __name__ == "__main__":
    main()