"""Примеры использования type hints в Python."""

from typing import List, Dict, Optional, Union, Tuple


# ✅ Простые типы
def greet(name: str) -> str:
    """Приветствие с типизацией."""
    return f"Hello, {name}!"


# ✅ Списки и словари
def process_numbers(numbers: List[int]) -> int:
    """Обработка списка чисел."""
    return sum(numbers)


def get_user_info() -> Dict[str, Union[str, int]]:
    """Возвращает информацию о пользователе."""
    return {
        "name": "Alice",
        "age": 30,
        "email": "alice@example.com"
    }


# ✅ Optional типы
def find_user(user_id: int) -> Optional[Dict[str, str]]:
    """Поиск пользователя. Может вернуть None."""
    users = {
        1: {"name": "Alice", "email": "alice@example.com"},
        2: {"name": "Bob", "email": "bob@example.com"}
    }
    return users.get(user_id)


# ✅ Tuple
def get_coordinates() -> Tuple[float, float]:
    """Возвращает координаты (широта, долгота)."""
    return (55.751244, 37.618423)


# ✅ Class с типизацией
class User:
    """Пользователь с type hints."""

    def __init__(self, name: str, age: int, email: str) -> None:
        self.name: str = name
        self.age: int = age
        self.email: str = email

    def get_info(self) -> Dict[str, Union[str, int]]:
        """Получить информацию о пользователе."""
        return {
            "name": self.name,
            "age": self.age,
            "email": self.email
        }

    def is_adult(self) -> bool:
        """Проверка совершеннолетия."""
        return self.age >= 18


# Использование
if __name__ == "__main__":
    print(greet("World"))
    print(process_numbers([1, 2, 3, 4, 5]))
    print(find_user(1))
    user = User("Alice", 30, "alice@example.com")
    print(user.get_info())
