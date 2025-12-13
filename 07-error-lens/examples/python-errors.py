"""Примеры ошибок Python для Error Lens."""

# ❌ Синтаксическая ошибка
def bad_function()  # Missing colon

# ❌ Ошибка отступов
def indent_error():
  x = 1
   y = 2  # Inconsistent indentation

# ❌ Неопределённая переменная
print(undefined_variable)  # NameError

# ❌ Неиспользуемый импорт
import os  # Unused import

# ❌ Неиспользуемая переменная
unused_var = 42

# ❌ Деление на ноль (runtime, но Pylance предупредит)
result = 10 / 0
