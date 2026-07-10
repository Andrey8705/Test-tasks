# -*- coding: utf-8 -*-
"""
ГЕНЕРАТОР ИНВЕСТИЦИОННЫХ ПРЕЗЕНТАЦИЙ
====================================
Читает финансовые показатели из ФЭМ (Excel), подставляет метаданные
проекта из config.py и собирает автономный HTML со слайдами и
диаграммами в стиле строительной компании (палитра «жжёная охра»).

Диаграммы рисуются инлайн-SVG прямо из данных — внешних библиотек нет,
файл остаётся автономным (можно открыть в браузере, распечатать в PDF,
переслать партнёрам).

Запуск:   python generate.py
Результат: presentation.html
"""

import base64
import html
import math
import os
import sys

import openpyxl

import config as cfg

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))

# ─────────────────────────────────────────────────────────────
# ПАЛИТРА (дизайн; менять здесь, не в config.py)
# ─────────────────────────────────────────────────────────────
OCHRE        = "#D9761F"   # основной акцент интерфейса (заголовки, рамки, номера)
OCHRE_LIGHT  = "#E9A85E"
OCHRE_DEEP   = "#9E5219"
CREAM        = "#F5ECE1"
# Матовая категориальная палитра для диаграмм (землистые тона, не «химозные»).
# Проверена валидатором CVD: разделение ΔE ~19; насыщенность намеренно
# приглушена, читаемость обеспечивают прямые подписи и легенды.
RAMP         = ["#C67E3C", "#4F9585", "#A277AC"]   # глина-охра · сине-зелёный · пыльно-лиловый
BAR_RETURN   = "#C67E3C"   # доход (тёплый охровый)
BAR_PRINCIPAL = "#4F9585"  # тело инвестиции (приглушённый сине-зелёный — контраст к доходу)


# ─────────────────────────────────────────────────────────────
# ЧТЕНИЕ EXCEL
# ─────────────────────────────────────────────────────────────
def read_financials():
    path = os.path.join(HERE, cfg.EXCEL_FILE)
    if not os.path.exists(path):
        sys.exit(f"[ОШИБКА] Не найден файл ФЭМ: {path}")
    wb = openpyxl.load_workbook(path, data_only=True)

    def cell(spec):
        sheet, coord = spec
        if sheet not in wb.sheetnames:
            sys.exit(f"[ОШИБКА] В книге нет листа '{sheet}'. "
                     f"Проверьте CELLS в config.py. Листы: {wb.sheetnames}")
        val = wb[sheet][coord].value
        if isinstance(val, str) and val.startswith(("#REF", "#NUM", "#N/A", "#VALUE")):
            sys.exit(f"[ОШИБКА] Ячейка {sheet}!{coord} содержит ошибку Excel: {val}")
        return val

    raw = {k: cell(v) for k, v in cfg.CELLS.items()}
    rate = cfg.USD_RATE
    fin = {
        "revenue_usd":    raw["revenue_kzt"] / rate,
        "net_profit_usd": raw["net_profit_kzt"] / rate,
        "area_m2":        raw["sellable_area_m2"],
        "ros":            raw.get("ros"),
        "irr":            raw.get("irr"),
        "area_mix": [
            ("Офисы / Offices",   raw.get("area_office") or 0),
            ("Коммерция / Retail", raw.get("area_retail") or 0),
            ("Паркинг / Parking",  raw.get("area_parking") or 0),
        ],
        "_raw": raw,
    }
    fin["price_m2_usd"] = fin["revenue_usd"] / fin["area_m2"] if fin["area_m2"] else 0

    # Земельный участок
    ha = raw.get("land_area_ha") or 0
    price_sotka = raw.get("land_price_sotka_usd") or 0
    fin["land"] = {
        "ha": ha,
        "sotka": ha * 100,                 # 1 га = 100 соток
        "m2": ha * 10_000,
        "price_sotka_usd": price_sotka,
        "total_usd": ha * 100 * price_sotka,
        "floors": raw.get("floors") or 0,
    }
    fin["land"]["efficiency"] = (fin["area_m2"] / fin["land"]["m2"]) if fin["land"]["m2"] else 0
    return fin


# ─────────────────────────────────────────────────────────────
# ФОРМАТИРОВАНИЕ
# ─────────────────────────────────────────────────────────────
def usd_millions(v):
    m = v / 1_000_000
    return f"${m:.2f}M" if m < 10 else f"${m:.1f}M"


def usd_int(v):
    return f"${v:,.0f}"


def area_fmt(v):
    return f"{v:,.0f} m²"


def kpi_value(key, fin):
    return {
        "revenue":    usd_millions(fin["revenue_usd"]),
        "net_profit": usd_millions(fin["net_profit_usd"]),
        "area":       area_fmt(fin["area_m2"]),
        "price_m2":   usd_int(fin["price_m2_usd"]),
    }.get(key, "—")


def esc(s):
    return html.escape(str(s))


# ─────────────────────────────────────────────────────────────
# ДИАГРАММЫ (инлайн-SVG)
# ─────────────────────────────────────────────────────────────
def svg_donut(segments):
    """Кольцевая диаграмма «части целого» с центральной подписью."""
    r, sw, c = 84, 30, 120
    C = 2 * math.pi * r
    gap = 2.4
    total = sum(v for _, v in segments) or 1
    parts = [f'<circle cx="{c}" cy="{c}" r="{r}" fill="none" '
             f'stroke="rgba(255,255,255,.09)" stroke-width="{sw}"/>']
    off = 0.0
    for i, (label, val) in enumerate(segments):
        seg = val / total * C
        dash = max(seg - gap, 0.5)
        parts.append(
            f'<circle cx="{c}" cy="{c}" r="{r}" fill="none" stroke="{RAMP[i % len(RAMP)]}" '
            f'stroke-width="{sw}" stroke-dasharray="{dash:.2f} {C - dash:.2f}" '
            f'stroke-dashoffset="{-off:.2f}" transform="rotate(-90 {c} {c})">'
            f'<title>{esc(label)}: {val:,.0f} m² ({val/total*100:.0f}%)</title></circle>')
        off += seg
    center = sum(v for _, v in segments)
    parts.append(
        f'<text x="{c}" y="{c-6}" text-anchor="middle" fill="{CREAM}" '
        f'font-size="30" font-weight="800">{center:,.0f}</text>'
        f'<text x="{c}" y="{c+18}" text-anchor="middle" fill="rgba(245,236,225,.6)" '
        f'font-size="13" letter-spacing="1.5">m² GLA</text>')
    return (f'<svg viewBox="0 0 240 240" width="100%" height="100%" '
            f'role="img" aria-label="Структура площадей">{"".join(parts)}</svg>')


def donut_legend(segments):
    total = sum(v for _, v in segments) or 1
    rows = ""
    for i, (label, val) in enumerate(segments):
        rows += (f'<div class="lg-row"><span class="lg-dot" style="background:{RAMP[i % len(RAMP)]}"></span>'
                 f'<span class="lg-name">{esc(label)}</span>'
                 f'<span class="lg-val">{val:,.0f} m² · {val/total*100:.0f}%</span></div>')
    return f'<div class="legend">{rows}</div>'


def svg_payout_bar(principal, income, scale_max):
    """Горизонтальный стек: тело + доход, ширина в масштабе max(итог)."""
    W, H = 320, 22
    total = principal + income
    pw = principal / scale_max * W
    iw = income / scale_max * W
    gap = 2
    return (
        f'<svg viewBox="0 0 {W} {H}" width="100%" height="{H}" preserveAspectRatio="none" '
        f'role="img" aria-label="Структура выплаты">'
        f'<rect x="0" y="0" width="{max(pw-gap,1):.1f}" height="{H}" rx="4" fill="{BAR_PRINCIPAL}">'
        f'<title>Тело / Principal: {usd_int(principal)}</title></rect>'
        f'<rect x="{pw:.1f}" y="0" width="{max(iw,1):.1f}" height="{H}" rx="4" fill="{BAR_RETURN}">'
        f'<title>Доход / Return: {usd_int(income)}</title></rect>'
        f'</svg>')


def svg_landbars(m2, gla):
    """Две горизонтальные полосы: площадь участка vs продаваемая площадь (GLA)."""
    W, H = 340, 168
    scale = max(m2, gla) or 1
    rows = [("Участок / Plot", m2, RAMP[1]), ("Продаваемая площадь / GLA", gla, RAMP[0])]
    parts = [f'<svg viewBox="0 0 {W} {H}" width="100%" height="auto" role="img" aria-label="Эффективность застройки">']
    for i, (label, val, color) in enumerate(rows):
        y = 14 + i * 86
        bw = max(val / scale * W, 4)
        parts.append(f'<text x="0" y="{y}" fill="rgba(245,236,225,.62)" font-size="14">{esc(label)}</text>')
        parts.append(f'<rect x="0" y="{y+12}" width="{bw:.1f}" height="40" rx="8" fill="{color}"/>')
        parts.append(f'<text x="{min(bw-10, W-10):.1f}" y="{y+38}" text-anchor="end" fill="#241204" '
                     f'font-size="17" font-weight="800">{val:,.0f} m²</text>')
    parts.append("</svg>")
    return "".join(parts)


def svg_gantt(timeline):
    """Диаграмма Ганта по этапам проекта."""
    def midx(ym):
        y, m = map(int, ym.split("-"))
        return y * 12 + (m - 1)

    starts = [midx(t["start"]) for t in timeline]
    ends = [midx(t["end"]) for t in timeline]
    m0, m1 = min(starts), max(ends)
    span = (m1 - m0 + 1)

    W, L, R, T = 1060, 8, 8, 14
    plot_w = W - L - R
    row_h, row_gap = 46, 16
    rows_top = T + 26
    H = rows_top + len(timeline) * (row_h + row_gap) + 34

    def x_of(mi, edge=0):     # edge=0 начало месяца, 1 — конец
        return L + (mi - m0 + edge) / span * plot_w

    svg = [f'<svg viewBox="0 0 {W} {H}" width="100%" height="100%" '
           f'role="img" aria-label="Сроки проекта">']

    # вертикальные линии по кварталам + подписи месяцев
    mi = m0
    while mi <= m1 + 1:
        y_ = mi // 12
        mo = mi % 12
        x = x_of(mi)
        if mo % 3 == 0:
            svg.append(f'<line x1="{x:.1f}" y1="{rows_top-8}" x2="{x:.1f}" y2="{H-24}" '
                       f'stroke="rgba(255,255,255,.10)" stroke-width="1"/>')
            svg.append(f'<text x="{x+4:.1f}" y="{H-8}" fill="rgba(245,236,225,.55)" '
                       f'font-size="12">{mo+1:02d}.{str(y_)[2:]}</text>')
        mi += 1

    for i, t in enumerate(timeline):
        y = rows_top + i * (row_h + row_gap)
        x0 = x_of(midx(t["start"]), 0)
        x1 = x_of(midx(t["end"]), 1)
        bw = max(x1 - x0 - 3, 6)
        color = RAMP[i % len(RAMP)]
        svg.append(
            f'<rect x="{x0:.1f}" y="{y:.1f}" width="{bw:.1f}" height="{row_h}" rx="8" '
            f'fill="{color}"><title>{esc(t["phase_ru"])}: {esc(t["period_ru"])}</title></rect>')
        # подпись фазы на баре (или рядом, если бар узкий) — только рус. название,
        # англ. дублируется в описании ниже
        label = esc(t["phase_ru"])
        if bw > 150:
            svg.append(f'<text x="{x0+16:.1f}" y="{y+row_h/2-2:.1f}" fill="#2a1607" '
                       f'font-size="15" font-weight="700">{label}</text>'
                       f'<text x="{x0+16:.1f}" y="{y+row_h/2+16:.1f}" fill="rgba(42,22,7,.72)" '
                       f'font-size="12">{esc(t["period_ru"])}</text>')
        else:
            svg.append(f'<text x="{x1+12:.1f}" y="{y+row_h/2+5:.1f}" fill="{CREAM}" '
                       f'font-size="14" font-weight="700">{label} '
                       f'<tspan fill="rgba(245,236,225,.6)">{esc(t["period_ru"])}</tspan></text>')
    svg.append("</svg>")
    return "".join(svg)


# ─────────────────────────────────────────────────────────────
# СЛАЙДЫ
# ─────────────────────────────────────────────────────────────
def footer(P, page):
    return (f'<div class="foot"><span>{esc(P["brand"])} © {P["year"]}</span>'
            f'<span class="pageno">{page}</span></div>')


def build_slides(fin):
    P = cfg.PROJECT
    n = 0

    def num():
        nonlocal n
        n += 1
        return f"{n:02d}"

    # ── 1. Титул ──
    s1 = f"""
    <section class="slide slide--title">
      <div class="kicker"><span class="kicker-mark"></span>{esc(P['eyebrow_en'])} <span class="sep">/</span> {esc(P['eyebrow_ru'])}</div>
      <h1 class="title">{esc(P['title'])}</h1>
      <p class="subtitle">{esc(P['subtitle_ru'])} <span class="dot">•</span> {esc(P['subtitle_en'])}</p>
      <div class="title-facts">
        <div class="fact"><p><b>Локация:</b> {esc(P['location_ru'])}</p><p><b>Формат:</b> {esc(P['format_ru'])}</p></div>
        <div class="fact"><p><b>Location:</b> {esc(P['location_en'])}</p><p><b>Format:</b> {esc(P['format_en'])}</p></div>
      </div>
      {footer(P, num())}
    </section>"""

    # ── 2. Земельный участок ──
    ld = fin["land"]
    land_cards = [
        (f'{ld["ha"]:g} га', f'ПЛОЩАДЬ УЧАСТКА / LAND AREA · {ld["m2"]:,.0f} m²'),
        (usd_int(ld["price_sotka_usd"]), 'ЦЕНА ЗА СОТКУ / PRICE PER SOTKA (USD)'),
        (usd_millions(ld["total_usd"]), 'СТОИМОСТЬ УЧАСТКА / LAND VALUE (USD)'),
        (f'{ld["floors"]:g}', 'ЭТАЖНОСТЬ / FLOORS'),
    ]
    lc = "".join(f'<div class="kpi-card"><div class="kpi-value">{esc(v)}</div>'
                 f'<div class="kpi-label">{esc(l)}</div></div>' for v, l in land_cards)
    s_land = f"""
    <section class="slide">
      <h2 class="section-title">Земельный участок <span class="sep">/</span> Land Plot</h2>
      <div class="econ-grid">
        <div class="kpi-grid">{lc}</div>
        <div class="chart-card">
          <div class="chart-head">Эффективность застройки <span class="sep">/</span> Buildable Efficiency</div>
          <div class="donut-wrap" style="align-items:flex-start">{svg_landbars(ld['m2'], fin['area_m2'])}</div>
          <div class="chips"><span class="chip">Плотность застройки / Density <b>×{ld['efficiency']:.1f}</b></span></div>
        </div>
      </div>
      {footer(P, num())}
    </section>"""

    # ── 3. Экономика + пончик ──
    cards = ""
    for k in P["kpi"]:
        val = k["value"] if k["value"] is not None else kpi_value(k["key"], fin)
        cards += (f'<div class="kpi-card"><div class="kpi-value">{esc(val)}</div>'
                  f'<div class="kpi-label">{esc(k["label_ru"])} / {esc(k["label_en"])}</div></div>')
    chips = ""
    if fin.get("ros") is not None:
        chips += f'<span class="chip">ROS <b>{fin["ros"]*100:.0f}%</b></span>'
    if fin.get("irr") is not None:
        chips += f'<span class="chip">IRR <b>{fin["irr"]:.1f}</b></span>'
    s2 = f"""
    <section class="slide">
      <h2 class="section-title">Экономика проекта <span class="sep">/</span> Project Economics (USD)</h2>
      <div class="econ-grid">
        <div class="kpi-grid">{cards}</div>
        <div class="chart-card">
          <div class="chart-head">Структура площадей <span class="sep">/</span> Area Mix</div>
          <div class="donut-wrap"><div class="donut">{svg_donut(fin['area_mix'])}</div>{donut_legend(fin['area_mix'])}</div>
          <div class="chips">{chips}</div>
        </div>
      </div>
      {footer(P, num())}
    </section>"""

    # ── 3. Оффер + стек-бары ──
    totals = [o["investment"] + o["investment"] * o["rate"] * o["months"] / 12
              for o in P["offer_options"]]
    scale_max = max(totals) if totals else 1
    opts = ""
    for o in P["offer_options"]:
        income = o["investment"] * o["rate"] * o["months"] / 12
        total = o["investment"] + income
        opts += f"""
        <div class="offer-card">
          <div class="offer-head">{esc(o['title_ru'])} <span class="sep">/</span> {esc(o['title_en'])}</div>
          <div class="offer-row"><span class="offer-sub">ИНВЕСТИЦИИ / INVESTMENT</span>
            <span class="offer-rate">{o['rate']*100:.0f}% годовых / p.a.</span></div>
          <div class="offer-invest">{usd_int(o['investment'])}</div>
          <div class="offer-sub" style="margin-top:14px">Выплата через {o['months']} мес. / Total Payout</div>
          <div class="offer-payout">{usd_int(total)} <span class="cur">USD</span></div>
          <div class="bar">{svg_payout_bar(o['investment'], income, scale_max)}</div>
          <div class="bar-legend">
            <span><i style="background:{BAR_PRINCIPAL}"></i>Тело / Principal {usd_millions(o['investment'])}</span>
            <span><i style="background:{BAR_RETURN}"></i>Доход / Return {usd_int(income)}</span>
          </div>
        </div>"""
    s3 = f"""
    <section class="slide">
      <h2 class="section-title">Инвестиционный оффер <span class="sep">/</span> Investment Offer</h2>
      <div class="offer-grid">{opts}</div>
      <div class="security-card">
        <div class="security-head"><span class="shield">◆</span> ГАРАНТИИ / SECURITY</div>
        <p>{esc(P['security_ru'])}</p>
        <p class="en">{esc(P['security_en'])}</p>
      </div>
      {footer(P, num())}
    </section>"""

    # ── 4. Сроки: Гант + описания ──
    phases = ""
    for i, t in enumerate(P["timeline"]):
        phases += (f'<div class="phase"><span class="phase-idx" style="background:{RAMP[i % len(RAMP)]}"></span>'
                   f'<div><div class="phase-title">{esc(t["phase_ru"])} / {esc(t["phase_en"])}</div>'
                   f'<div class="phase-text">{esc(t["text_ru"])}</div>'
                   f'<div class="phase-text en">{esc(t["text_en"])}</div></div></div>')
    s4 = f"""
    <section class="slide">
      <h2 class="section-title">Сроки и этапы <span class="sep">/</span> Timeline &amp; Key Milestones</h2>
      <div class="gantt">{svg_gantt(P['timeline'])}</div>
      <div class="phases">{phases}</div>
      {footer(P, num())}
    </section>"""

    return [s1, s_land, s2, s3, s4]


# ─────────────────────────────────────────────────────────────
# HTML-ОБОЛОЧКА
# ─────────────────────────────────────────────────────────────
def data_uri(rel_path):
    path = os.path.join(HERE, rel_path)
    if not os.path.exists(path):
        sys.exit(f"[ОШИБКА] Не найдено фоновое изображение: {path}")
    ext = os.path.splitext(path)[1].lstrip(".").lower()
    mime = "jpeg" if ext in ("jpg", "jpeg") else ext
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    return f"data:image/{mime};base64,{b64}"


def render_html(fin):
    P = cfg.PROJECT
    slide_list = build_slides(fin)
    slides = "\n".join(slide_list)
    bg = data_uri(P["background"])
    dots = "".join(f'<button class="dot-nav" data-i="{i}"></button>' for i in range(len(slide_list)))

    return f"""<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(P['title'])} — {esc(P['eyebrow_ru'])}</title>
<style>
  :root {{
    --ochre: {OCHRE};
    --ochre-light: {OCHRE_LIGHT};
    --cream: {CREAM};
    --text: {CREAM};
    --muted: rgba(245,236,225,.62);
    --card-border: rgba(233,168,94,.28);
    --card-fill: rgba(255,255,255,.045);
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  html, body {{ height: 100%; }}
  body {{
    background: #0f0805;
    font-family: 'Segoe UI', system-ui, -apple-system, Roboto, Helvetica, Arial, sans-serif;
    color: var(--text); -webkit-font-smoothing: antialiased;
  }}
  .deck {{ height: 100vh; overflow-y: scroll; scroll-snap-type: y mandatory; scroll-behavior: smooth; }}
  .slide {{
    position: relative; height: 100vh; scroll-snap-align: start;
    padding: 6vh 7vw 9vh; display: flex; flex-direction: column;
    background-image:
      linear-gradient(180deg, rgba(58,30,12,.55) 0%, rgba(36,19,9,.86) 52%, rgba(15,8,5,.97) 100%),
      url('{bg}');
    background-size: cover; background-position: center;
  }}
  .slide--title {{ justify-content: center; }}
  b {{ font-weight: 700; }}

  h1, h2, .kpi-value, .offer-invest, .offer-payout {{ font-weight: 800; letter-spacing: -0.01em; }}

  /* kicker / title */
  .kicker {{ display: flex; align-items: center; gap: 12px; letter-spacing: .3em;
    font-size: clamp(11px,1.05vw,14px); font-weight: 700; color: var(--muted); margin-bottom: 3.5vh; }}
  .kicker-mark {{ width: 26px; height: 3px; background: var(--ochre); display: inline-block; }}
  .kicker .sep {{ opacity: .5; }}
  .title {{ font-size: clamp(46px,6.6vw,98px); line-height: .98; }}
  .title::after {{ content:""; display:block; width:84px; height:5px; background:var(--ochre); margin-top:26px; border-radius:3px; }}
  .subtitle {{ font-size: clamp(16px,1.9vw,26px); font-weight: 400; margin: 22px 0 5vh; }}
  .subtitle .dot {{ color: var(--ochre); }}
  .title-facts {{ display: grid; grid-template-columns: 1fr 1fr; gap: 3vw; max-width: 1020px; }}
  .fact {{ border-left: 3px solid var(--ochre); padding-left: 18px; }}
  .fact p {{ font-size: clamp(13px,1.15vw,17px); line-height: 1.75; }}

  /* section title */
  .section-title {{ font-size: clamp(24px,3vw,40px); border-left: 5px solid var(--ochre);
    padding-left: 20px; margin-bottom: 4vh; flex: 0 0 auto; }}
  .section-title .sep, .offer-head .sep, .chart-head .sep {{ color: var(--ochre); font-weight: 400; }}

  /* KPI + econ layout */
  .econ-grid {{ display: grid; grid-template-columns: 1.15fr .85fr; gap: 26px; flex: 1; min-height: 0; }}
  .kpi-grid {{ display: grid; grid-template-columns: 1fr 1fr; grid-auto-rows: 1fr; gap: 18px; }}
  .kpi-card {{ border: 1px solid var(--card-border); background: var(--card-fill);
    border-radius: 14px; padding: 26px 30px; display: flex; flex-direction: column; justify-content: center;
    position: relative; overflow: hidden; }}
  .kpi-card::before {{ content:""; position:absolute; left:0; top:0; bottom:0; width:4px; background:var(--ochre); }}
  .kpi-value {{ font-size: clamp(30px,4vw,54px); line-height: 1; margin-bottom: 10px; }}
  .kpi-label {{ font-size: clamp(10px,1vw,13px); letter-spacing: .05em; color: var(--muted); text-transform: uppercase; }}

  .chart-card {{ border: 1px solid var(--card-border); background: var(--card-fill);
    border-radius: 14px; padding: 22px 26px; display: flex; flex-direction: column; }}
  .chart-head {{ font-size: clamp(13px,1.2vw,16px); font-weight: 700; color: var(--muted); margin-bottom: 8px; }}
  .donut-wrap {{ display: flex; align-items: center; gap: 18px; flex: 1; min-height: 0; }}
  .donut {{ width: 46%; max-width: 210px; aspect-ratio: 1; }}
  .legend {{ display: flex; flex-direction: column; gap: 12px; flex: 1; }}
  .lg-row {{ display: flex; align-items: center; gap: 9px; font-size: clamp(11px,1vw,14px); }}
  .lg-dot {{ width: 11px; height: 11px; border-radius: 3px; flex: 0 0 auto; }}
  .lg-name {{ font-weight: 600; }}
  .lg-val {{ margin-left: auto; color: var(--muted); }}
  .chips {{ display: flex; gap: 10px; margin-top: 14px; }}
  .chip {{ border: 1px solid var(--card-border); border-radius: 999px; padding: 6px 14px;
    font-size: 12px; letter-spacing: .06em; color: var(--muted); }}
  .chip b {{ color: var(--ochre-light); margin-left: 4px; }}

  /* offer */
  .offer-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }}
  .offer-card {{ border: 1px solid var(--card-border); background: var(--card-fill); border-radius: 14px; padding: 24px 28px; }}
  .offer-head {{ font-size: clamp(12px,1.15vw,16px); font-weight: 700; letter-spacing: .03em; color: var(--muted); margin-bottom: 16px; }}
  .offer-row {{ display: flex; justify-content: space-between; align-items: baseline; }}
  .offer-sub {{ font-size: clamp(10px,1vw,13px); letter-spacing: .05em; color: var(--muted); }}
  .offer-rate {{ font-size: clamp(12px,1.1vw,15px); font-weight: 700; color: var(--ochre-light); }}
  .offer-invest {{ font-size: clamp(28px,3.2vw,44px); margin: 2px 0; }}
  .offer-payout {{ font-size: clamp(24px,2.7vw,38px); color: var(--ochre-light); margin: 2px 0 14px; }}
  .offer-payout .cur {{ font-size: .5em; color: var(--muted); font-weight: 600; }}
  .bar {{ margin: 4px 0 10px; }}
  .bar-legend {{ display: flex; justify-content: space-between; gap: 10px; font-size: clamp(10px,.95vw,12.5px); color: var(--muted); }}
  .bar-legend i {{ display: inline-block; width: 10px; height: 10px; border-radius: 3px; margin-right: 6px; vertical-align: middle; }}
  .security-card {{ border: 1px solid var(--card-border); background: rgba(217,118,31,.09); border-radius: 14px; padding: 18px 26px; margin-top: 22px; }}
  .security-head {{ font-size: clamp(12px,1.05vw,15px); font-weight: 700; letter-spacing: .05em; color: var(--ochre-light); margin-bottom: 8px; }}
  .security-head .shield {{ margin-right: 6px; }}
  .security-card p {{ font-size: clamp(12px,1.05vw,15px); line-height: 1.5; }}
  .security-card .en {{ color: var(--muted); margin-top: 4px; }}

  /* timeline */
  .gantt {{ flex: 0 0 auto; margin-bottom: 3vh; }}
  .phases {{ display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 22px; }}
  .phase {{ display: flex; gap: 12px; }}
  .phase-idx {{ width: 6px; border-radius: 3px; flex: 0 0 auto; }}
  .phase-title {{ font-weight: 700; font-size: clamp(13px,1.15vw,16px); margin-bottom: 6px; }}
  .phase-text {{ font-size: clamp(11px,1vw,13.5px); line-height: 1.5; color: var(--text); }}
  .phase-text.en {{ color: var(--muted); margin-top: 4px; }}

  /* footer + nav */
  .foot {{ position: absolute; left: 7vw; right: 7vw; bottom: 4vh; display: flex; justify-content: space-between;
    font-size: 12px; color: var(--muted); letter-spacing: .04em; }}
  .pageno {{ font-weight: 700; color: var(--ochre-light); }}
  .nav {{ position: fixed; right: 22px; top: 50%; transform: translateY(-50%); display: flex; flex-direction: column; gap: 12px; z-index: 20; }}
  .dot-nav {{ width: 11px; height: 11px; border-radius: 50%; border: 1.5px solid rgba(233,168,94,.6); background: transparent; cursor: pointer; padding: 0; transition: .2s; }}
  .dot-nav.active {{ background: var(--ochre); border-color: var(--ochre); transform: scale(1.15); }}

  @media print {{
    @page {{ size: 1280px 720px; margin: 0; }}
    .deck {{ height: auto; overflow: visible; }}
    .slide {{ height: 720px; width: 1280px; page-break-after: always; }}
    .nav {{ display: none; }}
  }}
</style>
</head>
<body data-palette="{','.join(RAMP)}">
  <div class="deck" id="deck">
    {slides}
  </div>
  <div class="nav">{dots}</div>
<script>
  const deck = document.getElementById('deck');
  const slides = [...document.querySelectorAll('.slide')];
  const dots = [...document.querySelectorAll('.dot-nav')];
  let cur = 0;
  const go = i => {{ cur = Math.max(0, Math.min(slides.length-1, i)); slides[cur].scrollIntoView({{behavior:'smooth'}}); }};
  dots.forEach(d => d.addEventListener('click', () => go(+d.dataset.i)));
  document.addEventListener('keydown', e => {{
    if (['ArrowDown','ArrowRight','PageDown',' '].includes(e.key)) {{ e.preventDefault(); go(cur+1); }}
    if (['ArrowUp','ArrowLeft','PageUp'].includes(e.key)) {{ e.preventDefault(); go(cur-1); }}
    if (e.key === 'Home') go(0); if (e.key === 'End') go(slides.length-1);
  }});
  const io = new IntersectionObserver(es => es.forEach(en => {{
    if (en.isIntersecting) {{ cur = slides.indexOf(en.target); dots.forEach((d,i)=>d.classList.toggle('active', i===cur)); }}
  }}), {{threshold:.6}});
  slides.forEach(s => io.observe(s));
</script>
</body>
</html>"""


# ─────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────
def main():
    fin = read_financials()
    out = os.path.join(HERE, "presentation.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(render_html(fin))
    print("Готово! Файл:", out)
    print(f"\nИзвлечено из ФЭМ (курс {cfg.USD_RATE:.1f} ₸/$):")
    print(f"  Общая выручка    : {usd_millions(fin['revenue_usd']):>10}   ({fin['_raw']['revenue_kzt']:,.0f} ₸)")
    print(f"  Чистая прибыль   : {usd_millions(fin['net_profit_usd']):>10}   ({fin['_raw']['net_profit_kzt']:,.0f} ₸)")
    print(f"  Площадь к продаже: {area_fmt(fin['area_m2']):>10}")
    print(f"  Цена за м²       : {usd_int(fin['price_m2_usd']):>10}")
    print(f"  Структура площадей: " + ", ".join(f"{l.split(' /')[0]} {v:,.0f}" for l, v in fin['area_mix']))
    if fin.get("ros") is not None:
        print(f"  (справочно) ROS  : {fin['ros']*100:.1f}%   IRR: {fin['irr']:.2f}")


if __name__ == "__main__":
    main()
