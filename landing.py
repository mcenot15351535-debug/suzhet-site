#!/usr/bin/env python3
"""Сюжет — лендинг инвестиционного проекта.

Локально:   python landing.py  →  http://127.0.0.1:8000
На хостинге: переменные PORT задаёт платформа.
"""

from __future__ import annotations

import os

from flask import Flask, Response

app = Flask(__name__)

# ------------------------------- контент ----------------------------------

HERO = [
    ("2 млн ₽", "нужны инвестиции"),
    ("81%", "IRR проекта"),
    ("+2,85 млн ₽", "NPV за 3 года"),
    ("≈ 1 год", "срок окупаемости"),
]

STEPS = [
    ("Товар", "Аренда зала и техники", "цена = себестоимость", False, "s1"),
    ("Услуга", "Организация корпоратива", "цена = час работы", False, "s2"),
    ("Впечатление", "Иммерсивный сюжет", "цена = эмоция и память", True, "s3"),
    ("Трансформация", "Команда меняется", "эффект измеряем: eNPS до и после", True, "s4"),
]

B2B = [
    ("Мероприятий в год", "30"),
    ("Средний чек", "280 тыс. ₽"),
    ("Переменные затраты", "190 тыс. ₽"),
    ("Вклад одного", "90 тыс. ₽"),
    ("Вклад в год", "2,70 млн ₽"),
]

EVE = [
    ("Вечеров в год", "20"),
    ("Билетов × цена", "65 × 2 500 ₽"),
    ("Переменные затраты", "100 тыс. ₽"),
    ("Вклад одного", "62,5 тыс. ₽"),
    ("Вклад в год", "1,25 млн ₽"),
]

INVEST = [
    ("Реквизит и декор", 700),
    ("Свет и звук", 600),
    ("Сайт, CRM, бренд", 300),
    ("Запуск маркетинга", 200),
    ("Резерв", 200),
]

FLOW = [
    ("Вклад B2B и вечеров", 3950, "gold"),
    ("Постоянные затраты", 2000, "coral"),
    ("Свободный поток", 1950, "plum"),
]

NPV = [
    ("Поток, тыс. ₽", ["−2 000", "1 950", "1 950", "1 955"], True),
    ("Коэффициент при 10%", ["1,000", "0,909", "0,826", "0,751"], False),
    ("Приведённая стоимость", ["−2 000", "1 773", "1 612", "1 465"], False),
]

SENS = [
    ("Средний чек B2B", 760, 4938),
    ("Переменные затраты B2B", 1432, 4267),
    ("Билеты × цена билета", 2041, 3658),
    ("Число B2B-мероприятий", 2178, 3521),
    ("Постоянные затраты", 2352, 3347),
    ("Переменные вечеров", 2352, 3347),
    ("Число вечеров", 2539, 3160),
    ("Ставка дисконтирования", 2765, 2936),
]

BE = [
    ("B2B-мероприятий в год", "30", "17", "−42%"),
    ("Средний чек B2B", "280 тыс. ₽", "242 тыс. ₽", "−14%"),
    ("Переменные затраты B2B", "190 тыс. ₽", "228 тыс. ₽", "+20%"),
    ("Билетов на вечер", "65", "42", "−35%"),
    ("Цена билета", "2 500 ₽", "1 619 ₽", "−35%"),
    ("Постоянные затраты", "2,00 млн ₽", "3,15 млн ₽", "+57%"),
    ("Ставка дисконтирования", "10%", "81%", "×8"),
]

SCEN = [
    ["История", "бюджеты режут", "план сбылся", "формат «зашёл»"],
    ["B2B: мероприятий × чек", "22 × 260 тыс.", "30 × 280 тыс.", "38 × 290 тыс."],
    ["Вечера: шт × билетов", "16 × 55", "20 × 65", "24 × 75"],
    ["Цена билета", "2 300 ₽", "2 500 ₽", "2 700 ₽"],
    ["Ставка", "14%", "10%", "10%"],
    ["Годовой поток", "−274 тыс. ₽", "+1 950 тыс. ₽", "+3 990 тыс. ₽"],
    ["NPV", "−2,64 млн ₽", "+2,85 млн ₽", "+7,92 млн ₽"],
]

HIST = [
    (-5.5, 0.1), (-4.1, 1.1), (-2.8, 5.2), (-1.4, 14.4),
    (-0.1, 23.5), (1.3, 24.7), (2.6, 17.0), (3.9, 9.0),
    (5.3, 3.7), (6.6, 1.1), (8.0, 0.2), (9.3, 0.0),
]

# --------------------------------- стили ----------------------------------

CSS = """
:root{--ink:#241128;--plum:#6B2A63;--gold:#E9B44C;--coral:#E4573D;--cream:#F6EEE1;
--line:rgba(36,17,40,.12)}
*{box-sizing:border-box;margin:0}
body{font-family:ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif;
background:var(--cream);color:var(--ink);-webkit-font-smoothing:antialiased;line-height:1.5}
.wrap{max-width:1080px;margin:0 auto;padding:0 20px}
section{padding:72px 0}
.eyebrow{font-size:11px;letter-spacing:.22em;text-transform:uppercase;color:#6B2A63;opacity:.8}
h2{font-size:clamp(28px,4vw,44px);line-height:1.05;letter-spacing:-.02em;margin:10px 0 16px}
p.lead{color:rgba(36,17,40,.65);max-width:640px}
.hero{background:var(--ink);color:var(--cream);padding:96px 0 72px}
.hero .eyebrow{color:var(--gold)}
h1{font-size:clamp(56px,11vw,112px);line-height:.86;letter-spacing:-.03em;margin:16px 0}
.kpis{display:grid;grid-template-columns:repeat(2,1fr);gap:28px;
border-top:1px solid rgba(246,238,225,.15);padding-top:32px;margin-top:48px}
@media(min-width:720px){.kpis{grid-template-columns:repeat(4,1fr)}}
.kpi b{display:block;font-size:26px;color:var(--gold)}
.kpi span{font-size:13px;color:rgba(246,238,225,.6)}
.btn{display:inline-block;border-radius:999px;padding:12px 22px;font-size:14px;font-weight:600;
text-decoration:none;background:var(--gold);color:var(--ink);margin-top:32px}
.grid{display:grid;gap:18px}
@media(min-width:720px){.grid.two{grid-template-columns:1fr 1fr}
.grid.four{grid-template-columns:repeat(4,1fr)}}
.card{border:1px solid var(--line);border-radius:18px;padding:20px;background:#fff9;margin-top:24px}
.card h3{font-size:17px;margin-bottom:12px}
.row{display:flex;justify-content:space-between;gap:16px;padding:8px 0;
border-bottom:1px solid var(--line);font-size:14px}
.row:last-child{border-bottom:0}
.row span:first-child{color:rgba(36,17,40,.6)}
.row b{font-variant-numeric:tabular-nums}
.dark{background:var(--ink);color:var(--cream)}
.dark h2{color:var(--cream)}
.dark .lead{opacity:.6}
table{width:100%;border-collapse:collapse;font-size:14px;margin-top:24px;
font-variant-numeric:tabular-nums}
th,td{padding:12px;text-align:right;border-top:1px solid var(--line)}
th{color:rgba(36,17,40,.55);font-weight:500;border-top:0}
th:first-child,td:first-child{text-align:left}
.dark table th,.dark table td{border-color:rgba(246,238,225,.14)}
.dark table th{color:rgba(246,238,225,.55)}
tr.hot{background:rgba(233,180,76,.14)}
.bar{height:8px;border-radius:999px;background:rgba(36,17,40,.08);overflow:hidden;margin-top:6px}
.bar i{display:block;height:100%;border-radius:999px;background:var(--gold)}
.bar i.coral{background:var(--coral)}
.bar i.plum{background:var(--plum)}
.steps{display:grid;gap:12px;align-items:end;margin-top:32px}
@media(min-width:720px){.steps{grid-template-columns:repeat(4,1fr)}}
.step{border-radius:18px;padding:20px;display:flex;flex-direction:column;
justify-content:space-between}
.s1{background:#EADFC8;height:200px}
.s2{background:#DCC6D9;height:250px}
.s3{background:#7A2E5E;color:var(--cream);height:310px}
.s4{background:var(--ink);color:var(--cream);height:370px}
.step .tag{font-size:10px;letter-spacing:.18em;text-transform:uppercase;opacity:.6}
.step b{display:block;font-size:17px;line-height:1.2;margin-top:6px}
.step p{font-size:13px;opacity:.7;margin-top:14px}
.badge{display:inline-block;background:var(--gold);color:var(--ink);font-size:10px;
font-weight:700;letter-spacing:.1em;text-transform:uppercase;border-radius:999px;
padding:4px 10px;margin-bottom:12px}
.sens{display:grid;gap:8px;margin-top:28px}
.sens .lab{font-size:14px;color:rgba(36,17,40,.75)}
.track{position:relative;height:16px;margin-top:4px}
.track:before{content:"";position:absolute;left:0;right:0;top:50%;height:1px;
background:var(--line)}
.track i{position:absolute;top:0;height:16px}
.track i.neg{background:var(--coral);border-radius:4px 0 0 4px}
.track i.pos{background:var(--plum);border-radius:0 4px 4px 0}
.track u{position:absolute;top:-4px;width:1px;height:24px;background:rgba(36,17,40,.45)}
.note{display:inline-block;margin-top:24px;padding:10px 16px;border-radius:12px;
background:rgba(228,87,61,.1);color:#8A2A18;font-size:14px;font-weight:500}
.hist{display:flex;align-items:flex-end;gap:6px;height:220px;margin-top:32px}
.hist div{flex:1;display:flex;flex-direction:column;justify-content:flex-end;height:100%}
.hist b{font-size:10px;color:rgba(246,238,225,.45);text-align:center;margin-bottom:4px}
.hist i{display:block;border-radius:4px 4px 0 0;background:var(--gold)}
.hist i.neg{background:var(--coral)}
.mini{display:grid;gap:12px}
@media(min-width:720px){.mini{grid-template-columns:repeat(2,1fr)}}
.cta{margin-top:40px;background:var(--ink);color:var(--cream);border-radius:24px;
padding:48px 32px}
.cta p.big{font-size:clamp(22px,3.4vw,36px);font-weight:600;line-height:1.15;
max-width:640px;margin-top:12px}
footer{border-top:1px solid var(--line);padding:32px 0;font-size:12px;
color:rgba(36,17,40,.5)}
"""

# ------------------------------- рендеринг --------------------------------


def fmt(n: int) -> str:
    return f"{n:,}".replace(",", " ")


def pairs(data) -> str:
    return "".join(
        f'<div class="row"><span>{k}</span><b>{v}</b></div>' for k, v in data
    )


def build_page() -> str:
    hero = "".join(
        f'<div class="kpi"><b>{v}</b><span>{l}</span></div>' for v, l in HERO
    )

    steps = "".join(
        f'<div class="step {cls}"><div>'
        f'{"<span class=badge>Наш продукт</span>" if mine else ""}'
        f'<div class="tag">{tag}</div><b>{title}</b></div><p>{sub}</p></div>'
        for tag, title, sub, mine, cls in STEPS
    )

    invest = "".join(
        f'<div class="row" style="border:0;padding:6px 0">'
        f"<span>{n}</span><b>{v} тыс.</b></div>"
        f'<div class="bar"><i style="width:{v / 700 * 100:.0f}%"></i></div>'
        for n, v in INVEST
    )

    flow = "".join(
        f'<div class="row" style="border:0;padding:6px 0">'
        f"<span>{n}</span><b>{fmt(v)}</b></div>"
        f'<div class="bar"><i class="{cls}" style="width:{v / 3950 * 100:.0f}%"></i></div>'
        for n, v, cls in FLOW
    )

    npv = "".join(
        f"<tr><td>{label}</td>"
        + "".join(
            f'<td{" style=color:#E9B44C;font-weight:600" if strong else ""}>{c}</td>'
            for c in cells
        )
        + "</tr>"
        for label, cells, strong in NPV
    )

    base, lo, hi = 2849, 700, 5000

    def pct(x: float) -> float:
        return (x - lo) / (hi - lo) * 100

    sens = "".join(
        f'<div class="lab">{name}</div><div class="track">'
        f'<i class="neg" style="left:{pct(l):.1f}%;width:{pct(base) - pct(l):.1f}%"></i>'
        f'<i class="pos" style="left:{pct(base):.1f}%;width:{pct(h) - pct(base):.1f}%"></i>'
        f'<u style="left:{pct(base):.1f}%"></u></div>'
        for name, l, h in SENS
    )

    be = "".join(
        f'<tr{" class=hot" if i == 1 else ""}>'
        f"<td>{n}</td><td>{b}</td><td><b>{z}</b></td><td>{g}</td></tr>"
        for i, (n, b, z, g) in enumerate(BE)
    )

    scen = "".join(
        "<tr>"
        + "".join(
            f'<td{" style=color:#E9B44C;font-weight:600" if ri == len(SCEN) - 1 else ""}>{c}</td>'
            for c in row
        )
        + "</tr>"
        for ri, row in enumerate(SCEN)
    )

    peak = max(p for _, p in HIST)
    hist = "".join(
        f'<div><b>{p if p else ""}</b>'
        f'<i class="{"neg" if x < 0 else ""}" '
        f'style="height:{max(2, p / peak * 100):.0f}%"></i></div>'
        for x, p in HIST
    )

    return f"""<!doctype html>
<html lang="ru"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Сюжет — иммерсивная ивент-студия, Екатеринбург</title>
<meta name="description" content="Иммерсивная ивент-студия «Сюжет»: NPV +2,85 млн за 3 года, IRR 81%, окупаемость около года. Привлекаем 2 млн ₽.">
<meta property="og:title" content="Сюжет — мы продаём не мероприятие, а впечатление">
<meta property="og:description" content="NPV +2,85 млн ₽ за 3 года, IRR 81%, окупаемость ≈ 1 год. Привлекаем 2 млн ₽.">
<meta property="og:type" content="website">
<style>{CSS}</style></head><body>

<div class="hero"><div class="wrap">
  <div class="eyebrow">Иммерсивная ивент-студия • Екатеринбург</div>
  <h1>Сюжет</h1>
  <p style="font-size:20px;opacity:.75;max-width:520px">
    Мы продаём не мероприятие, а впечатление.</p>
  <div class="kpis">{hero}</div>
  <a class="btn" href="#npv">Смотреть расчёт</a>
</div></div>

<section><div class="wrap">
  <div class="eyebrow">Слайд 2</div>
  <h2>Экономика впечатлений: ценность растёт</h2>
  <p class="lead">Компании покупают не услугу, а изменение состояния команды.
  Мы работаем на двух верхних ступенях и измеряем результат опросом до и после.</p>
  <div class="steps">{steps}</div>
</div></section>

<section style="padding-top:0"><div class="wrap">
  <div class="eyebrow">Слайд 3</div>
  <h2>Две опоры: B2B и билетные вечера</h2>
  <div class="grid two">
    <div class="card"><h3>Корпоративные заказы</h3>{pairs(B2B)}</div>
    <div class="card"><h3>Билетные вечера</h3>{pairs(EVE)}</div>
  </div>
  <div class="card" style="background:var(--ink);color:var(--cream);border:0">
    <div class="row" style="border:0">
      <span style="color:rgba(246,238,225,.6)">Выручка в год</span>
      <b style="font-size:22px">11,65 млн ₽</b></div>
    <div class="bar" style="height:12px;background:rgba(246,238,225,.12)">
      <i style="width:72%;border-radius:999px 0 0 999px"></i>
      <i style="width:28%;background:var(--plum);border-radius:0 999px 999px 0"></i></div>
    <div class="row" style="border:0;font-size:12px;opacity:.6">
      <span>B2B 8,4 млн · 72%</span><span>вечера 3,25 млн</span></div>
  </div>
</div></section>

<section style="padding-top:0"><div class="wrap">
  <div class="eyebrow">Слайд 4</div>
  <h2>Куда идут деньги и что они приносят</h2>
  <div class="grid two">
    <div class="card"><h3>Инвестиции · 2,0 млн ₽</h3>{invest}</div>
    <div class="card"><h3>Годовой поток · тыс. ₽</h3>{flow}
      <p style="margin-top:16px;font-size:13px;color:rgba(36,17,40,.6)">
      30 × 90 + 20 × 62,5 − 2 000 = 1 950</p></div>
  </div>
  <p class="lead" style="margin-top:16px;font-size:14px">Постоянные затраты: команда 1,30 ·
  склад и офис 0,25 · маркетинг 0,30 · прочее 0,15 млн ₽</p>
</div></section>

<section class="dark" id="npv"><div class="wrap">
  <div class="eyebrow" style="color:var(--gold)">Слайд 5</div>
  <h2>Базовый расчёт NPV за три года</h2>
  <table><thead><tr><th></th><th>Год 0</th><th>Год 1</th><th>Год 2</th><th>Год 3</th></tr></thead>
  <tbody>{npv}</tbody></table>
  <p style="margin-top:16px;font-size:14px;opacity:.6">
  Σ приведённых потоков 4 849 − 2 000 = NPV +2 849 тыс. ₽</p>
  <div class="kpis">
    <div class="kpi"><b>+2,85 млн ₽</b><span>NPV за 3 года</span></div>
    <div class="kpi"><b>≈ 81%</b><span>IRR проекта</span></div>
    <div class="kpi"><b>≈ 1 год</b><span>срок окупаемости</span></div>
    <div class="kpi"><b>+2,12 млн ₽</b><span>NPV после УСН 15%</span></div>
  </div>
</div></section>

<section><div class="wrap">
  <div class="eyebrow">Слайд 6</div>
  <h2>Чувствительность: каждый параметр ±10%</h2>
  <p class="lead">Коралловый — NPV ниже базы, сливовый — выше. Риска — база +2 849 тыс. ₽.</p>
  <div class="sens">{sens}</div>
  <div class="note">Главный рычаг — средний чек: −10% к чеку забирает 73% NPV.</div>
</div></section>

<section style="padding-top:0"><div class="wrap">
  <div class="eyebrow">Слайд 7</div>
  <h2>Точки безубыточности: где NPV равен нулю</h2>
  <table><thead><tr><th>Параметр</th><th>База</th><th>NPV = 0</th><th>Запас</th></tr></thead>
  <tbody>{be}</tbody></table>
  <p class="lead" style="margin-top:16px;font-size:14px">Узкое место — чек: запас всего 14%.
  Поэтому пакеты вместо скидок и фиксированные цены у подрядчиков.</p>
</div></section>

<section class="dark"><div class="wrap">
  <div class="eyebrow" style="color:var(--gold)">Слайд 8</div>
  <h2>Три сценария: три цельные истории</h2>
  <table><thead><tr><th></th><th>Пессимистичный</th><th>Базовый</th>
  <th>Оптимистичный</th></tr></thead><tbody>{scen}</tbody></table>
  <p class="lead" style="margin-top:16px;font-size:14px">
  Веса 25 / 50 / 25 → ожидаемый NPV <b style="color:var(--gold)">+2,75 млн ₽</b></p>
</div></section>

<section class="dark" style="padding-top:0"><div class="wrap">
  <div class="eyebrow" style="color:var(--gold)">Слайд 9</div>
  <h2>Монте-Карло: как часто проект проигрывает</h2>
  <p class="lead">10 000 случайных прогонов: все параметры меняются одновременно.</p>
  <div class="hist">{hist}</div>
  <div class="mini" style="margin-top:32px">
    <div class="card" style="background:rgba(246,238,225,.05);
    border-color:rgba(246,238,225,.12)"><h3 style="color:var(--gold)">22%</h3>
      <p style="font-size:13px;opacity:.6">прогонов с NPV &lt; 0</p></div>
    <div class="card" style="background:rgba(246,238,225,.05);
    border-color:rgba(246,238,225,.12)"><h3 style="color:var(--gold)">+1,64 млн ₽</h3>
      <p style="font-size:13px;opacity:.6">средний NPV</p></div>
    <div class="card" style="background:rgba(246,238,225,.05);
    border-color:rgba(246,238,225,.12)"><h3 style="color:var(--gold)">−1,7 … +5,3 млн ₽</h3>
      <p style="font-size:13px;opacity:.6">90% исходов</p></div>
    <div class="card" style="background:rgba(246,238,225,.05);
    border-color:rgba(246,238,225,.12)"><h3 style="color:var(--gold)">10 000</h3>
      <p style="font-size:13px;opacity:.6">прогонов Монте-Карло</p></div>
  </div>
</div></section>

<section><div class="wrap">
  <div class="eyebrow">Слайд 10</div>
  <h2>Как мы защищаем ваши деньги</h2>
  <div class="mini">
    <div class="card"><h3 style="color:var(--plum);font-size:24px">50%</h3>
      <p style="font-size:14px;color:rgba(36,17,40,.65)">
      предоплата от B2B-клиента до мероприятия</p></div>
    <div class="card"><h3 style="color:var(--plum);font-size:24px">65%</h3>
      <p style="font-size:14px;color:rgba(36,17,40,.65)">
      вложений остаются имуществом: реквизит, свет и звук</p></div>
    <div class="card"><h3 style="color:var(--plum);font-size:24px">−22%</h3>
      <p style="font-size:14px;color:rgba(36,17,40,.65)">
      антикризисный план: постоянные 2,05 → 1,6 млн, поток ≥ 0</p></div>
    <div class="card"><h3 style="color:var(--plum);font-size:24px">+2,75 млн ₽</h3>
      <p style="font-size:14px;color:rgba(36,17,40,.65)">
      ожидаемый NPV при весах 25 / 50 / 25</p></div>
  </div>
  <div class="cta">
    <div class="eyebrow" style="color:var(--gold)">Предложение</div>
    <p class="big">Вложите 2 млн ₽ — получите NPV +2,85 млн, IRR 81%
    и возврат примерно за год.</p>
    <a class="btn" href="mailto:hello@suzhet.studio?subject=Инвестиции%20в%20студию%20«Сюжет»">
    Обсудить инвестицию</a>
  </div>
</div></section>

<footer><div class="wrap">
  © 2026 Сюжет — иммерсивная ивент-студия, Екатеринбург · Показатели — расчётная
  финансовая модель на допущениях проекта, а не гарантия доходности.
  Вероятность убытка по Монте-Карло — 22%.
</div></footer>
</body></html>"""


# -------------------------------- маршруты --------------------------------

PAGE = build_page()


@app.get("/")
def index() -> Response:
    response = Response(PAGE, mimetype="text/html; charset=utf-8")
    response.headers["Cache-Control"] = "public, max-age=300"
    return response


@app.get("/healthz")
def healthz() -> Response:
    return Response("ok", mimetype="text/plain")


@app.after_request
def security_headers(response: Response) -> Response:
    response.headers.setdefault("X-Content-Type-Options", "nosniff")
    response.headers.setdefault("X-Frame-Options", "SAMEORIGIN")
    response.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
    return response


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    try:
        from waitress import serve
    except ImportError:
        app.run(host="0.0.0.0", port=port)
    else:
        serve(app, host="0.0.0.0", port=port, threads=4)
