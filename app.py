
from contextlib import closing
from datetime import datetime, timezone
from pathlib import Path
import sqlite3

from flask import Flask, jsonify, request

app = Flask(__name__)
app.json.ensure_ascii = False
DB_PATH = Path(__file__).with_name("ads.db")


def connect_db():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    with closing(connect_db()) as connection:
        with connection:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS ads (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    owner TEXT NOT NULL
                )
            """)


def get_json_dict():
    """Получаем JSON-объект или None, если клиент передал не объект."""
    data = request.get_json(silent=True)
    return data if isinstance(data, dict) else None


@app.post("/ads")
def create_ad():
    data = get_json_dict()
    required = ("title", "description", "owner")
    if data is None or any(
        not isinstance(data.get(field), str) or not data[field].strip()
        for field in required
    ):
        return jsonify(error="Нужны непустые строки: title, description, owner"), 400

    created_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    with closing(connect_db()) as connection:
        with connection:
            cursor = connection.execute(
                "INSERT INTO ads (title, description, created_at, owner) VALUES (?, ?, ?, ?)",
                (data["title"].strip(), data["description"].strip(), created_at,
                 data["owner"].strip()),
            )
            ad_id = cursor.lastrowid
        row = connection.execute("SELECT * FROM ads WHERE id = ?", (ad_id,)).fetchone()
    return jsonify(dict(row)), 201


@app.get("/ads")
def list_ads():
    with closing(connect_db()) as connection:
        rows = connection.execute("SELECT * FROM ads ORDER BY id").fetchall()
    return jsonify([dict(row) for row in rows]), 200


@app.get("/ads/<int:ad_id>")
def get_ad(ad_id):
    with closing(connect_db()) as connection:
        row = connection.execute("SELECT * FROM ads WHERE id = ?", (ad_id,)).fetchone()
    if row is None:
        return jsonify(error="Объявление не найдено"), 404
    return jsonify(dict(row)), 200


@app.patch("/ads/<int:ad_id>")
def update_ad(ad_id):
    data = get_json_dict()
    allowed_fields = {"title", "description"}
    if not data or not set(data).issubset(allowed_fields):
        return jsonify(error="Укажите title и/или description"), 400
    if any(not isinstance(value, str) or not value.strip() for value in data.values()):
        return jsonify(error="Значения должны быть непустыми строками"), 400

    with closing(connect_db()) as connection:
        old_ad = connection.execute("SELECT * FROM ads WHERE id = ?", (ad_id,)).fetchone()
        if old_ad is None:
            return jsonify(error="Объявление не найдено"), 404
        title = data.get("title", old_ad["title"])
        description = data.get("description", old_ad["description"])
        with connection:
            connection.execute(
                "UPDATE ads SET title = ?, description = ? WHERE id = ?",
                (title.strip(), description.strip(), ad_id),
            )
        updated = connection.execute("SELECT * FROM ads WHERE id = ?", (ad_id,)).fetchone()
    return jsonify(dict(updated)), 200


@app.delete("/ads/<int:ad_id>")
def delete_ad(ad_id):
    with closing(connect_db()) as connection:
        with connection:
            cursor = connection.execute("DELETE FROM ads WHERE id = ?", (ad_id,))
    if cursor.rowcount == 0:
        return jsonify(error="Объявление не найдено"), 404
    return "", 204


init_db()

if __name__ == "__main__":
    app.run(debug=True)  # Только для локальной разработки!
