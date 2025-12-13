"""Тесты для примеров Python."""

import pytest
from typing import List, Dict


def test_addition():
    """Тест сложения."""
    assert 2 + 2 == 4


def test_string_methods():
    """Тест методов строк."""
    text = "Hello, World!"
    assert text.upper() == "HELLO, WORLD!"
    assert text.lower() == "hello, world!"
    assert text.split(",") == ["Hello", " World!"]


def test_list_operations():
    """Тест операций со списками."""
    numbers = [1, 2, 3]
    numbers.append(4)
    assert numbers == [1, 2, 3, 4]
    assert sum(numbers) == 10


def test_dict_operations():
    """Тест операций со словарями."""
    user: Dict[str, str] = {"name": "Alice", "email": "alice@example.com"}
    assert user.get("name") == "Alice"
    assert "name" in user.keys()


@pytest.fixture
def sample_users() -> List[Dict[str, str]]:
    """Фикстура с тестовыми данными."""
    return [
        {"name": "Alice", "email": "alice@example.com"},
        {"name": "Bob", "email": "bob@example.com"},
    ]


def test_with_fixture(sample_users):
    """Тест с использованием фикстуры."""
    assert len(sample_users) == 2
    assert sample_users[0]["name"] == "Alice"


class TestUserClass:
    """Тесты для класса User."""

    def test_user_creation(self):
        """Тест создания пользователя."""
        user = {"name": "Charlie", "age": 25}
        assert user["name"] == "Charlie"
        assert user["age"] == 25

    def test_user_methods(self):
        """Тест методов пользователя."""
        users = [{"name": "Alice"}, {"name": "Bob"}]
        names = [u["name"] for u in users]
        assert "Alice" in names
        assert "Bob" in names
