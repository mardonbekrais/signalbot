import sqlite3
import os

DB_PATH = "scheduled_messages.db"

def init_db():
    """Ma'lumotlar bazasi va jadvalni yaratish."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message_text TEXT,
            target_chat_id INTEGER,
            schedule_time TIMESTAMP,
            is_sent BOOLEAN DEFAULT FALSE
        )
    ''')
    conn.commit()
    conn.close()

def add_message(text, chat_id, schedule_time):
    """Yangi xabarni bazaga qo'shish."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO messages (message_text, target_chat_id, schedule_time) VALUES (?, ?, ?)",
        (text, chat_id, schedule_time)
    )
    conn.commit()
    conn.close()

def get_pending_messages():
    """Yuborilishi kerak bo'lgan xabarlarni olish."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM messages WHERE is_sent = FALSE AND schedule_time <= datetime('now')")
    messages = cursor.fetchall()
    conn.close()
    return messages

def mark_as_sent(message_id):
    """Xabarni yuborilgan deb belgilash."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE messages SET is_sent = TRUE WHERE id = ?", (message_id,))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Ma'lumotlar bazasi muvaffaqiyatli yaratildi.")
