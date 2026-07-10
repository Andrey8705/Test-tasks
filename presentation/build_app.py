# -*- coding: utf-8 -*-
"""
СБОРЩИК ОФЛАЙН-ПРИЛОЖЕНИЯ
=========================
Встраивает библиотеку SheetJS (чтение .xlsx в браузере) и фоновое
изображение по умолчанию в один самодостаточный файл app.html.

Запуск:   python build_app.py
Результат: app.html  — открывается двойным кликом, работает без интернета.
"""

import base64
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))

TEMPLATE = os.path.join(HERE, "app_template.html")
SHEETJS = os.path.join(HERE, "node_modules", "xlsx", "dist", "xlsx.full.min.js")
BG = os.path.join(HERE, "assets", "building.jpg")
OUT = os.path.join(HERE, "app.html")


def data_uri(path):
    ext = os.path.splitext(path)[1].lstrip(".").lower()
    mime = "jpeg" if ext in ("jpg", "jpeg") else ext
    with open(path, "rb") as f:
        return f"data:image/{mime};base64," + base64.b64encode(f.read()).decode()


def main():
    for p in (TEMPLATE, SHEETJS, BG):
        if not os.path.exists(p):
            sys.exit(f"[ОШИБКА] Не найдено: {p}\n"
                     f"Для SheetJS выполните в папке presentation:\n"
                     f"  npm install https://cdn.sheetjs.com/xlsx-0.20.3/xlsx-0.20.3.tgz")

    html = open(TEMPLATE, encoding="utf-8").read()
    sheetjs = open(SHEETJS, encoding="utf-8").read()

    html = html.replace("/*__SHEETJS__*/", sheetjs)
    html = html.replace("__BG_DEFAULT__", data_uri(BG))

    with open(OUT, "w", encoding="utf-8") as f:
        f.write(html)

    size = os.path.getsize(OUT) / 1024
    print(f"Готово! Файл: {OUT}  ({size:,.0f} КБ)")
    print("Откройте app.html двойным кликом. Библиотека и пример встроены — интернет не нужен.")


if __name__ == "__main__":
    main()
