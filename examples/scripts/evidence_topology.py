#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Генератор SVG-схемы «Целевая топология» (раздел 4).

Вертикальный веер: клиенты -> шлюз сверху, от шлюза стрелки расходятся вниз к
четырём контурам сервисов (стоят рядом вертикальными колонками), затем сходятся
к слою данных и шины.

Запуск:  python3 examples/evidence_topology.py
Результат: examples/evidence_topology.svg
"""

import html
import os

HERE = os.path.dirname(os.path.abspath(__file__))

# --- геометрия ---------------------------------------------------------------
CANVAS_W = 1260
MARGIN = 40
COLS = 4
COL_GAP = 22
COL_W = (CANVAS_W - 2 * MARGIN - (COLS - 1) * COL_GAP) // COLS   # 278

CHIP_H, CHIP_GAP, PANEL_PAD, HEADER_H = 58, 10, 18, 34
MAX_CHIPS = 9
PANEL_TOP = 322
PANEL_H = PANEL_PAD + HEADER_H + MAX_CHIPS * CHIP_H + (MAX_CHIPS - 1) * CHIP_GAP + PANEL_PAD

CLIENTS_Y, CLIENTS_H = 104, 48
GW_Y, GW_H = 176, 58
CANVAS_CX = CANVAS_W / 2

DATA_Y = PANEL_TOP + PANEL_H + 62
DATA_H = 122
CANVAS_H = DATA_Y + DATA_H + 42

LINK = "#7b879e"


def esc(s):
    return html.escape(s, quote=True)


# --- данные ------------------------------------------------------------------
CLIENTS = "Клиенты: React SPA · PWA осмотра (offline) · внешние API-клиенты"

CONTOURS = [
    {
        "label": "Ядро домена", "hint": "system of record",
        "color": "#4f9e57", "fill": "#eef8ef",
        "services": [
            ("S03", "Tenant & Org", "тенанты / орг"),
            ("S04", "Engagement", "заявки"),
            ("S06", "Object Registry", "объекты"),
            ("S07", "Methodology Reg.", "методики"),
            ("S08", "References / Normative", "справочники"),
            ("S09", "Commission", "комиссия"),
            ("S10", "DTP Cases", "ДТП"),
        ],
    },
    {
        "label": "Вычисления / контроль", "hint": "",
        "color": "#5b5bc0", "fill": "#eef0fc",
        "services": [
            ("S16", "Calculation Core", "Rust, gRPC"),
            ("S17", "QA / Autoexpertise", "автоэкспертиза"),
            ("S11", "Market Data", "рыночные данные"),
            ("S12", "Source Archive", "WORM"),
            ("S13", "Provenance", "доказательства"),
            ("S24", "Document Generation", "генерация документов"),
            ("S25", "E-Signature", "ЭП / УКЭП"),
        ],
    },
    {
        "label": "ИИ / CV / Интеграции", "hint": "",
        "color": "#c98a2b", "fill": "#fff7ea",
        "services": [
            ("S18", "CV Inspection", "CV-анализ фото"),
            ("S19", "Document Recognition", "OCR документов"),
            ("S20", "AI Expert Orchestrator", "ИИ-оркестратор"),
            ("S21", "Knowledge & Retrieval", "база знаний / RAG"),
            ("S22", "Model Registry & Serving", "реестр / сервинг моделей"),
            ("S23", "AI Guardrails & PII", "guardrails / PII"),
            ("S26", "Integration Hub", "интеграции"),
            ("S27", "Inspection & Offline Sync", "осмотр / offline-sync"),
        ],
    },
    {
        "label": "Общие сервисы", "hint": "",
        "color": "#8a8a8a", "fill": "#f5f5f5",
        "services": [
            ("S02", "IAM / Identity", ""),
            ("S05", "Workflow / Process", ""),
            ("S14", "Audit Log", "hash-chain"),
            ("S15", "Media / File Storage", ""),
            ("S28", "Notifications", ""),
            ("S29", "Metering & Billing", ""),
            ("S30", "Public Data API", ""),
            ("S31", "Search", ""),
            ("S32", "Analytics / OLAP", ""),
        ],
    },
]

DATA_COLOR, DATA_FILL = "#8a5bb4", "#f7eefc"


# --- svg-помощники -----------------------------------------------------------
out = []
add = out.append


def rect(x, y, w, h, fill, stroke="none", sw=0, rx=8, extra=""):
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" '
            f'rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>')


def text(x, y, s, size, fill, weight="400", anchor="start", extra=""):
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}" '
            f'font-weight="{weight}" text-anchor="{anchor}" {extra}>{esc(s)}</text>')


def edge(x1, y1, x2, y2):
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{LINK}" stroke-width="2" marker-end="url(#arrow)"/>')


# --- каркас ------------------------------------------------------------------
add(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {CANVAS_W} {CANVAS_H}" '
    f'width="{CANVAS_W}" height="{CANVAS_H}" '
    f'font-family="Segoe UI, Helvetica Neue, Arial, sans-serif">')

add('<defs>'
    '<linearGradient id="card" x1="0" y1="0" x2="0" y2="1">'
    '<stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#f6f8fc"/>'
    '</linearGradient>'
    '<filter id="soft" x="-20%" y="-20%" width="140%" height="160%">'
    '<feDropShadow dx="0" dy="2.5" stdDeviation="3.5" flood-color="#243b6b" flood-opacity="0.12"/>'
    '</filter>'
    '<marker id="arrow" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="7.5" '
    'markerHeight="7.5" orient="auto-start-reverse">'
    '<path d="M0,0 L10,5 L0,10 z" fill="#7b879e"/></marker>'
    '</defs>')

add(rect(6, 6, CANVAS_W - 12, CANVAS_H - 12, "url(#card)", "#e3e8f0", 1.5, 20))

# заголовок
add(text(44, 52, "Целевая топология", 26, "#1f2937", "700"))
add(text(44, 78, "Клиенты → шлюз → контуры сервисов → данные/шина (fan-out / fan-in)",
         13, "#6b7280"))

# --- клиенты и шлюз ----------------------------------------------------------
cw = 620
add(rect(CANVAS_CX - cw / 2, CLIENTS_Y, cw, CLIENTS_H, "#e8eefc", "#5b7bb4", 1.6, 11,
         'filter="url(#soft)"'))
add(text(CANVAS_CX, CLIENTS_Y + 30, CLIENTS, 13, "#1b2a44", "600", "middle"))

gw_w = 360
add(rect(CANVAS_CX - gw_w / 2, GW_Y, gw_w, GW_H, "#fde8e8", "#c0504d", 1.7, 11,
         'filter="url(#soft)"'))
add(text(CANVAS_CX, GW_Y + 25, "S01  API Gateway / BFF", 14, "#5a1a1a", "700", "middle"))
add(text(CANVAS_CX, GW_Y + 43, "JWT · rate-limit · tenant routing", 10.5, "#8a3434",
         "400", "middle"))

add(edge(CANVAS_CX, CLIENTS_Y + CLIENTS_H, CANVAS_CX, GW_Y - 1))

# --- контуры-колонки (веер) --------------------------------------------------
col_cx = []
for i, c in enumerate(CONTOURS):
    x = MARGIN + i * (COL_W + COL_GAP)
    cx = x + COL_W / 2
    col_cx.append(cx)
    col, fill = c["color"], c["fill"]

    add(rect(x, PANEL_TOP, COL_W, PANEL_H, fill, col, 1.7, 15, 'filter="url(#soft)"'))
    add(f'<circle cx="{x + 20}" cy="{PANEL_TOP + 22}" r="5" fill="{col}"/>')
    add(text(x + 33, PANEL_TOP + 27, c["label"], 14, col, "700"))
    if c["hint"]:
        add(text(x + 33, PANEL_TOP + 42, f'({c["hint"]})', 10, col, "400"))
    add(f'<line x1="{x + 14}" y1="{PANEL_TOP + 52}" x2="{x + COL_W - 14}" '
        f'y2="{PANEL_TOP + 52}" stroke="{col}" stroke-width="1" opacity="0.28"/>')

    services = c["services"]
    block = len(services) * CHIP_H + (len(services) - 1) * CHIP_GAP
    max_block = MAX_CHIPS * CHIP_H + (MAX_CHIPS - 1) * CHIP_GAP
    top0 = PANEL_TOP + PANEL_PAD + HEADER_H + (max_block - block) / 2
    chip_w = COL_W - 2 * PANEL_PAD
    for j, (sid, en, ru) in enumerate(services):
        cy = top0 + j * (CHIP_H + CHIP_GAP)
        cxp = x + PANEL_PAD
        add(rect(cxp, cy, chip_w, CHIP_H, "#ffffff", col, 1.2, 9))
        add(f'<rect x="{cxp + 9:.1f}" y="{cy + 12:.1f}" width="3.6" '
            f'height="{CHIP_H - 24}" rx="1.8" fill="{col}"/>')
        add(text(cxp + 21, cy + 24, sid, 13.5, col, "700"))
        add(text(cxp + 21, cy + 43, en, 12, "#2f3742", "600"))
        if ru:
            add(text(cxp + 21, cy + 55, ru, 10.5, "#9aa3ae", "400"))

# --- слой данных -------------------------------------------------------------
add(rect(MARGIN, DATA_Y, CANVAS_W - 2 * MARGIN, DATA_H, DATA_FILL, DATA_COLOR, 1.7, 15,
         'filter="url(#soft)"'))
add(f'<circle cx="{MARGIN + 20}" cy="{DATA_Y + 22}" r="5" fill="{DATA_COLOR}"/>')
add(text(MARGIN + 33, DATA_Y + 27, "Хранилища и шина", 14, DATA_COLOR, "700"))

inner_pad = 26
box_y = DATA_Y + 38
box_h = DATA_H - 50
inner_w = (CANVAS_W - 2 * MARGIN) - 2 * inner_pad
store_w = inner_w * 0.66
bus_w = inner_w - store_w - 18
store_x = MARGIN + inner_pad
bus_x = store_x + store_w + 18

add(rect(store_x, box_y, store_w, box_h, "#ffffff", DATA_COLOR, 1.2, 10))
add(text(store_x + 16, box_y + 24, "Хранилища", 11.5, DATA_COLOR, "700"))
add(text(store_x + 16, box_y + 44, "PostgreSQL (+PostGIS, pgvector) · MongoDB · ClickHouse", 10.5, "#374151"))
add(text(store_x + 16, box_y + 59, "InfluxDB · Redis/Valkey · MinIO/S3 · OpenSearch · Vector DB", 10.5, "#374151"))

add(rect(bus_x, box_y, bus_w, box_h, "#ffffff", DATA_COLOR, 1.2, 10))
add(text(bus_x + 16, box_y + 24, "Шина", 11.5, DATA_COLOR, "700"))
add(text(bus_x + 16, box_y + 44, "RabbitMQ (tasks/events) +", 10, "#374151"))
add(text(bus_x + 16, box_y + 58, "append-only журнал (Kafka/Streams)", 10, "#374151"))

# --- веер: шлюз -> контуры, контуры -> данные --------------------------------
gw_bottom = GW_Y + GW_H
for cx in col_cx:
    add(edge(CANVAS_CX, gw_bottom, cx, PANEL_TOP - 2))

col_bottom = PANEL_TOP + PANEL_H
for cx in col_cx:
    add(edge(cx, col_bottom, CANVAS_CX, DATA_Y - 2))

# подписи (сбоку от веера, чтобы не перекрывать линии)
add(text(CANVAS_CX + gw_w / 2 + 14, GW_Y + GW_H - 8, "fan-out", 11, "#9aa3ae", "700", "start"))
add(text(CANVAS_CX + gw_w / 2 + 14, DATA_Y - 8, "fan-in", 11, "#9aa3ae", "700", "start"))

add('</svg>')

svg = "\n".join(out)
dest = os.path.join(HERE, "evidence_topology.svg")
with open(dest, "w", encoding="utf-8") as f:
    f.write(svg)
print("written:", dest, len(svg), "bytes")
