"""Пример Flask приложения с type hints и Pylance."""

from flask import Flask, jsonify, request
from typing import Dict, List, Optional, Any

app = Flask(__name__)

# Mock database
users_db: List[Dict[str, Any]] = [
    {"id": 1, "name": "Alice", "email": "alice@example.com"},
    {"id": 2, "name": "Bob", "email": "bob@example.com"}
]


@app.route("/")
def index() -> str:
    """Главная страница."""
    return "Flask App with Type Hints!"


@app.route("/api/users", methods=["GET"])
def get_users() -> Dict[str, List[Dict[str, Any]]]:
    """Получить всех пользователей."""
    return jsonify({"users": users_db})


@app.route("/api/users/<int:user_id>", methods=["GET"])
def get_user(user_id: int) -> tuple[Dict[str, Any], int]:
    """Получить пользователя по ID."""
    user: Optional[Dict[str, Any]] = next(
        (u for u in users_db if u["id"] == user_id), None
    )

    if user:
        return jsonify(user), 200
    return jsonify({"error": "User not found"}), 404


@app.route("/api/users", methods=["POST"])
def create_user() -> tuple[Dict[str, Any], int]:
    """Создать нового пользователя."""
    data: Dict[str, str] = request.get_json()

    new_user: Dict[str, Any] = {
        "id": len(users_db) + 1,
        "name": data.get("name"),
        "email": data.get("email")
    }

    users_db.append(new_user)
    return jsonify(new_user), 201


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
