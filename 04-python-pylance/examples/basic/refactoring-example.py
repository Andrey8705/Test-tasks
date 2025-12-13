"""Примеры рефакторинга с Pylance."""


# ✅ 1. Rename Symbol (F2)
# Попробуйте: поставьте курсор на "old_function_name" и нажмите F2
def old_function_name(x: int) -> int:
    """Старое имя функции."""
    return x * 2


result = old_function_name(5)


# ✅ 2. Extract Method (выделите код и Ctrl+Shift+R)
def process_user_data(users: list) -> None:
    """Обработка данных пользователей."""
    # Выделите эти 3 строки и используйте "Extract Method"
    for user in users:
        print(f"Name: {user['name']}")
        print(f"Email: {user['email']}")
        print("---")


# ✅ 3. Extract Variable
def calculate_total(items: list) -> float:
    """Расчёт итоговой суммы."""
    # Выделите "(item['price'] * item['quantity'])" и используйте "Extract Variable"
    total = sum(item["price"] * item["quantity"] for item in items)
    return total


# ✅ 4. Organize Imports (Shift+Alt+O)
# Pylance автоматически отсортирует и удалит неиспользуемые импорты
import os
import sys
from typing import List
from datetime import datetime
import json


# ✅ 5. Add Type Hints
# Pylance предложит добавить типы, если их нет
def add_numbers(a, b):  # Pylance подскажет добавить типы
    """Сложение чисел."""
    return a + b


# ✅ 6. Convert to f-string
# Pylance может конвертировать старый format в f-string
name = "Alice"
age = 30
# Старый способ (Pylance предложит конвертировать)
message = "Name: {}, Age: {}".format(name, age)
# Новый способ (f-string)
message_new = f"Name: {name}, Age: {age}"


# ✅ 7. Quick Fix (Ctrl+.)
# Pylance предложит быстрые исправления для проблем
class MyClass:
    """Пример класса."""

    def method_with_error(self):
        """Метод с неиспользуемой переменной."""
        unused_var = 42  # Pylance подсветит и предложит удалить
        return "OK"
