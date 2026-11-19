
from flask import Flask, jsonify, request
import os
import socket
import psycopg
from psycopg.rows import dict_row

app = Flask(__name__)


def get_db_connection():
    return psycopg.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME", "cloud_db"),
        user=os.getenv("DB_USER", "cloud_user"),
        password=os.getenv("DB_PASSWORD"),
        row_factory=dict_row,
        connect_timeout=5
    )


def init_db():
    with get_db_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id SERIAL PRIMARY KEY,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)


@app.route("/")
def home():
    return jsonify({
        "message": "Welcome to Multi-Tier Cloud Infrastructure",
        "application": "Flask Web Application",
        "instance": os.getenv("APP_INSTANCE", socket.gethostname()),
        "status": "Healthy"
    })


@app.route("/health")
def health():
    return jsonify({"status": "UP"}), 200


@app.route("/db-health")
def db_health():
    try:
        with get_db_connection() as conn:
            conn.execute("SELECT 1")

        return jsonify({
            "database": "PostgreSQL",
            "status": "Connected"
        }), 200

    except psycopg.Error:
        app.logger.exception("Database health check failed")
        return jsonify({
            "database": "PostgreSQL",
            "status": "Unavailable"
        }), 503


@app.route("/messages", methods=["POST"])
def create_message():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "JSON object is required"}), 400

    content = data.get("content")

    if not isinstance(content, str) or not content.strip():
        return jsonify({"error": "Content is required"}), 400

    with get_db_connection() as conn:
        message = conn.execute(
            """
            INSERT INTO messages (content)
            VALUES (%s)
            RETURNING id, content, created_at
            """,
            (content.strip(),)
        ).fetchone()

    return jsonify(message), 201


@app.route("/messages", methods=["GET"])
def get_messages():
    with get_db_connection() as conn:
        messages = conn.execute(
            """
            SELECT id, content, created_at
            FROM messages
            ORDER BY id
            """
        ).fetchall()

    return jsonify(messages), 200


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)

