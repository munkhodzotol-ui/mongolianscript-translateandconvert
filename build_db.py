import json
import sqlite3
import re
import time

def normalize_text(text: str) -> str:
    if not text:
        return ""
    text = text.strip().lower()
    return re.sub(r'[\u180A\u180B\u180C\u180D\u180E]', '', text)

def build_database():
    json_path = "dictionary_clean.json"
    db_path = "mongolian_dict.db"

    print(f"[*] Reading {json_path}...")
    start_time = time.time()

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("PRAGMA synchronous = OFF;")
    cursor.execute("PRAGMA journal_mode = MEMORY;")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS dictionary (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cyrillic_raw TEXT NOT NULL,
        cyrillic_normalized TEXT NOT NULL,
        bichig_raw TEXT,
        bichig_normalized TEXT
    );
    """)

    records = []
    for cyr, bichig in data.items():
        cyr_norm = normalize_text(cyr)
        bichig_raw = bichig if isinstance(bichig, str) else ""
        bichig_norm = normalize_text(bichig_raw)
        records.append((cyr, cyr_norm, bichig_raw, bichig_norm))

    cursor.executemany("""
        INSERT INTO dictionary (cyrillic_raw, cyrillic_normalized, bichig_raw, bichig_normalized)
        VALUES (?, ?, ?, ?);
    """, records)

    cursor.execute("CREATE INDEX IF NOT EXISTS idx_cyrillic ON dictionary(cyrillic_normalized);")
    conn.commit()
    conn.close()

    elapsed = time.time() - start_time
    print(f"[✓] SUCCESS: Created '{db_path}' with {len(records):,} words in {elapsed:.3f}s!")

if __name__ == "__main__":
    build_database()