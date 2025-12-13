# Python + Pylance

## 📋 Описание
Мощный language server для Python с IntelliSense, type checking и auto-imports.

## 🚀 Установка
1. Extensions → **"Python"** и **"Pylance"**
2. Установить Python: https://python.org
3. Создать venv: `python -m venv venv`

## ⚙️ Топ-15 настроек

```json
{
  "python.analysis.typeCheckingMode": "basic",
  "python.analysis.autoImportCompletions": true,
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "python.formatting.provider": "none",
  "[python]": {
    "editor.defaultFormatter": "ms-python.black-formatter",
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
      "source.organizeImports": "explicit"
    }
  },
  "python.testing.pytestEnabled": true,
  "python.testing.unittestEnabled": false
}
```

## 🔧 Команды

```bash
# Создать виртуальное окружение
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Установить зависимости
pip install -r requirements.txt

# Форматирование
black .

# Линтинг
pylint **/*.py

# Тесты
pytest
```

## 📚 Возможности
- 🎯 Умное автодополнение
- 🔍 Type checking
- 📦 Auto-imports
- 🔧 Рефакторинг

## 🔗 Ссылки
- [Python Docs](https://docs.python.org/)
- [Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance)

[⬅️ Назад](../README.md)
