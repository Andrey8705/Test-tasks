"""Unit тесты для Test Explorer."""

import pytest


def test_addition():
    """Тест сложения."""
    assert 1 + 1 == 2


def test_subtraction():
    """Тест вычитания."""
    assert 5 - 3 == 2


def test_multiplication():
    """Тест умножения."""
    assert 3 * 4 == 12


def test_division():
    """Тест деления."""
    assert 10 / 2 == 5


class TestStringMethods:
    """Тесты для строковых методов."""

    def test_upper(self):
        """Тест upper()."""
        assert "hello".upper() == "HELLO"

    def test_lower(self):
        """Тест lower()."""
        assert "WORLD".lower() == "world"

    def test_split(self):
        """Тест split()."""
        assert "a,b,c".split(",") == ["a", "b", "c"]
