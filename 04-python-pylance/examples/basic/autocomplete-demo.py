"""Демонстрация автодополнения и IntelliSense в Pylance."""

import json
from pathlib import Path
from typing import List, Dict


# ✅ Автодополнение методов класса
class UserManager:
    """Менеджер пользователей."""

    def __init__(self):
        self.users: List[Dict[str, str]] = []

    def add_user(self, name: str, email: str) -> None:
        """Добавить пользователя."""
        self.users.append({"name": name, "email": email})

    def get_user_by_name(self, name: str) -> Dict[str, str] | None:
        """Найти пользователя по имени."""
        for user in self.users:
            if user["name"] == name:
                return user
        return None

    def get_all_emails(self) -> List[str]:
        """Получить все email."""
        return [user["email"] for user in self.users]


# Попробуйте: создайте экземпляр и наберите "manager." - появится автодополнение!
manager = UserManager()
manager.add_user("Alice", "alice@example.com")
manager.add_user("Bob", "bob@example.com")

# ✅ Автодополнение для строк
text = "Hello, World!"
# Попробуйте: наберите "text." - увидите все методы строки
result = text.upper()  # IntelliSense покажет типы
result = text.split(",")  # IntelliSense знает, что вернёт List[str]

# ✅ Автодополнение для списков
numbers: List[int] = [1, 2, 3, 4, 5]
# Попробуйте: наберите "numbers." - увидите методы списка
numbers.append(6)
numbers.extend([7, 8, 9])

# ✅ Автодополнение для словарей
user_data: Dict[str, str] = {"name": "Alice", "email": "alice@example.com"}
# Попробуйте: наберите "user_data." - увидите методы словаря
user_data.get("name")
user_data.keys()

# ✅ Автодополнение для Path
file_path = Path("data.json")
# Попробуйте: наберите "file_path." - увидите все методы Path
file_path.exists()
file_path.read_text()

# ✅ Auto-imports - Pylance автоматически добавит import
# Попробуйте: наберите "datetime.now()" - Pylance предложит импортировать
from datetime import datetime

now = datetime.now()
print(f"Текущее время: {now}")
