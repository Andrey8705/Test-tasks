# -*- coding: utf-8 -*-
"""
КОНФИГУРАЦИЯ ПРЕЗЕНТАЦИИ
========================
Это единственный файл, который нужно править под нового клиента.
Разделы:
  1. EXCEL         — какой файл ФЭМ читать и из каких ячеек брать финансы
  2. USD_RATE      — курс тенге к доллару для пересчёта
  3. PROJECT       — метаданные проекта (название, локация, оффер, сроки)

После правок запустите:  python generate.py
"""

# ─────────────────────────────────────────────────────────────
# 1. ФАЙЛ ФИНМОДЕЛИ И МАППИНГ ЯЧЕЕК
# ─────────────────────────────────────────────────────────────
# Значения берутся из указанных листов/ячеек. Если структура ФЭМ
# изменится — поправьте адрес ячейки здесь, в одном месте.
EXCEL_FILE = "femodel.xlsx"

CELLS = {
    # показатель            (лист,              ячейка)   — значения в тенге (KZT)
    "revenue_kzt":          ("НДС расчет",       "C6"),   # Выручка с НДС
    "net_profit_kzt":       ("Dashboard все",    "C4"),   # Net Profit
    "sellable_area_m2":     ("Dashboard все",    "C25"),  # Продаваемая площадь, м²
    # ROS и IRR — опциональные метрики, если захотите вывести на слайд
    "ros":                  ("Dashboard все",    "C5"),   # ROS, доля
    "irr":                  ("Dashboard все",    "C8"),   # IRR
    # Структура площадей (для диаграммы на слайде «Экономика»), м²
    "area_office":          ("Dashboard все",    "L17"),  # Офисы
    "area_retail":          ("Dashboard все",    "L18"),  # Коммерция
    "area_parking":         ("Dashboard все",    "L19"),  # Паркинг
    # Земельный участок (слайд «Земля») — с листа PnL
    "land_price_sotka_usd": ("PnL все",          "B3"),   # Цена за сотку, USD
    "land_area_ha":         ("PnL все",          "B5"),   # Площадь ЗУ, га
    "floors":               ("PnL все",          "B6"),   # Этажность
}

# ─────────────────────────────────────────────────────────────
# 2. КУРС ВАЛЮТЫ  (KZT за 1 USD)
# ─────────────────────────────────────────────────────────────
# Все тенговые суммы делятся на этот курс для отображения в USD.
# В исходном тизере Oner использовался курс ≈ 522.6 (выручка = $20.5M).
# Поставьте актуальный курс на дату презентации.
USD_RATE = 522.6

# ─────────────────────────────────────────────────────────────
# 3. МЕТАДАННЫЕ ПРОЕКТА  (то, чего нет в ФЭМ — заполняется вручную)
# ─────────────────────────────────────────────────────────────
PROJECT = {
    # Брендинг / подвал
    "brand":        "ONER BY HAYAT",
    "year":         2026,
    "background":   "assets/building.jpg",   # фото объекта (jpg/png)

    # ── Слайд 1: Титул ──
    "eyebrow_en":   "INVESTMENT TEASER",
    "eyebrow_ru":   "ИНВЕСТИЦИОННЫЙ ТИЗЕР",
    "title":        "Oner by Hayat",
    "subtitle_ru":  "Бизнес-центр класса А в Алматы",
    "subtitle_en":  "Class A Business Center in Almaty",
    "location_ru":  "Угол улиц Толе би / Абдуллиных",
    "location_en":  "Tole Bi / Abdullinykh Str.",
    "format_ru":    "Премиальное 10-этажное офисное здание",
    "format_en":    "Premium 10-story office building",

    # ── Слайд 2: Экономика проекта ──
    # KPI-плитки. value=None → подставится из Excel (см. generate.py).
    # Можно менять порядок, подписи, добавлять свои плитки.
    "kpi": [
        {"key": "revenue",     "value": None, "label_ru": "ОБЩАЯ ВЫРУЧКА",        "label_en": "TOTAL REVENUE"},
        {"key": "area",        "value": None, "label_ru": "ПЛОЩАДЬ К ПРОДАЖЕ",    "label_en": "TOTAL AREA FOR SALE"},
        {"key": "net_profit",  "value": None, "label_ru": "ЧИСТАЯ ПРИБЫЛЬ ПРОЕКТА","label_en": "NET PROJECT PROFIT"},
        {"key": "price_m2",    "value": None, "label_ru": "ЦЕНА ЗА М²",           "label_en": "PRICE PER M² (USD)"},
    ],

    # ── Слайд 3: Инвестиционный оффер ──
    # Для каждой опции указывается тело и ставка — доход и итог считаются автоматически.
    "offer_options": [
        {
            "title_ru": "ОПЦИЯ 1: 1.5 ГОДА", "title_en": "OPTION 1: 1.5 YEARS",
            "investment": 2_000_000,   # тело инвестиции, USD
            "rate": 0.12,              # ставка годовых
            "months": 18,              # срок, мес
        },
        {
            "title_ru": "ОПЦИЯ 2: 2 ГОДА", "title_en": "OPTION 2: 2 YEARS",
            "investment": 2_000_000,
            "rate": 0.12,
            "months": 24,
        },
    ],
    "security_ru": "100% защита капитала коммерческой недвижимостью БЦ класса А. "
                   "Приоритетное право выплат из кэш-флоу проекта.",
    "security_en": "100% capital protection backed by Class A commercial real estate assets. "
                   "Priority distribution from project cash flow.",

    # ── Слайд 4: Сроки и этапы ──
    # start / end — в формате "ГГГГ-ММ" (используются для диаграммы Ганта).
    "timeline": [
        {"period_ru": "Июль — Сентябрь 2026", "period_en": "Jul — Sep 2026",
         "start": "2026-07", "end": "2026-09",
         "phase_ru": "Подготовка", "phase_en": "Preparation",
         "text_ru": "Подготовка площадки, вынос сетей, запуск фундаментных работ.",
         "text_en": "Site preparation, utility relocation, foundation work kick-off."},
        {"period_ru": "Октябрь 2026 — Август 2027", "period_en": "Oct 2026 — Aug 2027",
         "start": "2026-10", "end": "2027-08",
         "phase_ru": "Строительство", "phase_en": "Construction",
         "text_ru": "Монолитные работы (10 этажей), остекление, фасады, внутренние сети.",
         "text_en": "Concrete framework (10 stories), glazing, facades, MEP installations."},
        {"period_ru": "Сентябрь — Декабрь 2027", "period_en": "Sep — Dec 2027",
         "start": "2027-09", "end": "2027-12",
         "phase_ru": "Ввод и расчёт", "phase_en": "Commissioning",
         "text_ru": "Ввод БЦ в эксплуатацию, закрытие продаж лотов, полный расчёт с инвестором.",
         "text_en": "Building commissioning, sales closure, full investor principal + return payout."},
    ],
}
