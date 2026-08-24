from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from bot.database import DB_PATH

app = Flask(__name__)

@app.route('/')
def index():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM messages")
    messages = cursor.fetchall()
    conn.close()
    return render_template('index.html', messages=messages)

@app.route('/add', methods=['POST'])
def add():
    text = request.form['text']
    chat_id = request.form['chat_id']
    schedule_time = request.form['schedule_time']
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO messages (message_text, target_chat_id, schedule_time) VALUES (?, ?, ?)",
        (text, chat_id, schedule_time)
    )
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
