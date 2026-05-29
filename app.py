from flask import Flask, render_template, request
import sqlite3
from datetime import datetime

app = Flask(__name__)

DB_NAME = "portfolio.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS visitors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            visited_at TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def save_message(name, email, message):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO messages (name, email, message, created_at)
        VALUES (?, ?, ?, ?)
    """, (name, email, message, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    conn.commit()
    conn.close()


def add_visitor():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO visitors (visited_at)
        VALUES (?)
    """, (datetime.now().strftime("%Y-%m-%d %H:%M:%S"),))

    conn.commit()
    conn.close()


def get_visitor_count():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM visitors")
    count = cursor.fetchone()[0]

    conn.close()
    return count


@app.route("/", methods=["GET", "POST"])
def home():
    init_db()
    message_sent = False

    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")

        save_message(name, email, message)
        message_sent = True

    add_visitor()
    visitor_count = get_visitor_count()

    return render_template(
        "index.html",
        message_sent=message_sent,
        visitor_count=visitor_count
    )


if __name__ == "__main__":
    app.run(debug=True)