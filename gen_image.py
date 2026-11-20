#!/usr/bin/env python3
"""Render the front page for 20 November 2026 as a single 1024x1024 PNG.

Everything is drawn from scratch with Pillow: no templates, no fetched
assets, no network. The six stories and the ticker items are the day's
verified news, worded here in my own phrasing.
"""

import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PATH = os.path.join(HERE, "entry.png")

PAGE = 1024
MARGIN = 40
INK = (26, 32, 46)
PAPER = (247, 243, 234)
CARD = (255, 255, 255)
RULE = (26, 32, 46)
MUTED = (96, 100, 112)
RED = (178, 52, 40)
TEAL = (31, 110, 107)
GOLD = (176, 124, 30)
NAVY = (38, 68, 120)
PLUM = (110, 58, 96)
GREEN = (46, 110, 62)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def typeface(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


TITLE_FONT = typeface("DejaVuSerif-Bold.ttf", 56)
DATE_FONT = typeface("DejaVuSans.ttf", 21)
KICKER_FONT = typeface("DejaVuSans-Bold.ttf", 17)
HEAD_FONT = typeface("DejaVuSerif-Bold.ttf", 25)
BODY_FONT = typeface("DejaVuSans.ttf", 17)
TICKER_FONT = typeface("DejaVuSans-Bold.ttf", 16)
TICKER_BODY = typeface("DejaVuSans.ttf", 16)


def split_lines(text, font, max_width):
    """Greedy word wrap: returns a list of lines that fit max_width."""
    words = text.split()
    lines = []
    current = ""
    for word in words:
        trial = word if not current else current + " " + word
        if font.getlength(trial) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def text_block(draw, x, y, lines, font, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += leading
    return y


STORIES = [
    {
        "kicker": "UKRAINE",
        "accent": NAVY,
        "glyph": "bridge",
        "headline": "Kyiv's bridges hit in huge overnight barrage",
        "summary": (
            "Russia fires 110+ missiles and about 400 drones at Ukraine; "
            "at least eight people are killed and 28 hurt, and three "
            "bridges across the Dnipro are damaged."
        ),
    },
    {
        "kicker": "SUMMIT",
        "accent": RED,
        "glyph": "summit",
        "headline": "Peace declaration, no peace deal",
        "summary": (
            "Trump, Xi and Putin end their first three-way meeting with a "
            "four-point declaration on nuclear talks, UN reform, fuel and "
            "the ICC - but no breakthrough on Ukraine or Iran."
        ),
    },
    {
        "kicker": "MARKETS",
        "accent": GREEN,
        "glyph": "chart",
        "headline": "AI sell-off deepens worldwide",
        "summary": (
            "The S&P 500 falls about 2% for a fifth straight day and the "
            "Nikkei drops 4.8%, with SoftBank down 16%; Anthropic closes "
            "about 17% above its $83 IPO price."
        ),
    },
    {
        "kicker": "DEBT",
        "accent": TEAL,
        "glyph": "globe",
        "headline": "IMF: world debt nears 100% of GDP",
        "summary": (
            "Kristalina Georgieva warns at the APEC summit in Shenzhen "
            "that global public debt will soon reach 100% of GDP - the "
            "highest since World War II."
        ),
    },
    {
        "kicker": "GAMES",
        "accent": PLUM,
        "glyph": "gamepad",
        "headline": "GTA 6: biggest launch ever",
        "summary": (
            "Sensor Tower estimates $2.36bn from about 24.6 million "
            "copies on launch day, the biggest entertainment launch on "
            "record. Take-Two has not confirmed the figures."
        ),
    },
    {
        "kicker": "DEFENCE",
        "accent": GOLD,
        "glyph": "drone",
        "headline": "UK sends 1,000+ drones to Ukraine",
        "summary": (
            "Britain pledges more than 1,000 long-range drones in a "
            "£260m package as Kyiv's allies meet in Berlin and say "
            "Europe is ready to talk with Russia."
        ),
    },
]

TICKER_ITEMS = [
    "US Senate passes energy-permitting bill 62-33",
    "Trump pardons baseball legend Pete Rose posthumously",
    "Young Europeans strike in 25+ countries over living costs",
]


def draw_summit(draw, box, color):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    r = 13
    for dx, dy in ((-20, 10), (20, 10), (0, -14)):
        draw.ellipse((cx + dx - r, cy + dy - r, cx + dx + r, cy + dy + r),
                     outline=color, width=4)
    draw.line((cx - 20, cy + 10, cx, cy - 14), fill=color, width=3)
    draw.line((cx + 20, cy + 10, cx, cy - 14), fill=color, width=3)
    draw.line((cx - 20, cy + 10, cx + 20, cy + 10), fill=color, width=3)


def draw_bridge(draw, box, color):
    x0, y0, x1, y1 = box
    mid = (x0 + x1) // 2
    draw.arc((x0 + 4, y0 + 6, x1 - 4, y1 - 6), 180, 360, fill=color, width=4)
    draw.line((x0 + 6, y1 - 12, mid - 8, y1 - 12), fill=color, width=4)
    draw.line((mid + 8, y1 - 12, x1 - 6, y1 - 12), fill=color, width=4)
    draw.line((mid, y0 + 14, mid, y1 - 12), fill=color, width=3)
    draw.line((x0 + 14, y0 + 26, x0 + 14, y1 - 12), fill=color, width=3)
    draw.line((x1 - 14, y0 + 26, x1 - 14, y1 - 12), fill=color, width=3)


def draw_scales(draw, box, color):
    x0, y0, x1, y1 = box
    cx = (x0 + x1) // 2
    top = y0 + 8
    draw.line((cx, top, cx, y1 - 10), fill=color, width=4)
    draw.line((x0 + 8, top + 8, x1 - 8, top + 8), fill=color, width=4)
    for side in (-1, 1):
        px = cx + side * 22
        draw.line((px, top + 8, px, top + 22), fill=color, width=3)
        draw.arc((px - 12, top + 16, px + 12, top + 36), 0, 180,
                 fill=color, width=3)
    draw.line((x0 + 12, y1 - 10, x1 - 12, y1 - 10), fill=color, width=4)


def draw_chart(draw, box, color):
    x0, y0, x1, y1 = box
    base = y1 - 12
    heights = (16, 28, 22, 40)
    step = (x1 - x0 - 16) // 4
    for i, h in enumerate(heights):
        bx = x0 + 8 + i * step
        draw.rectangle((bx, base - h, bx + step - 8, base), fill=color)
    draw.line((x0 + 6, base - 46, x1 - 8, base - 52), fill=color, width=4)
    draw.polygon(((x1 - 8, base - 52), (x1 - 20, base - 50),
                  (x1 - 14, base - 40)), fill=color)


def draw_flame(draw, box, color):
    x0, y0, x1, y1 = box
    cx = (x0 + x1) // 2
    draw.polygon(((cx, y0 + 6), (cx + 18, y0 + 34), (cx + 8, y0 + 34),
                  (cx + 16, y1 - 12), (cx - 16, y1 - 12), (cx - 8, y0 + 34),
                  (cx - 18, y0 + 34)), fill=color)
    draw.ellipse((cx - 6, y0 + 30, cx + 6, y0 + 44), fill=PAPER)


def draw_globe(draw, box, color):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    r = 24
    draw.ellipse((cx - r, cy - r, cx + r, cy + r), outline=color, width=4)
    draw.ellipse((cx - 11, cy - r, cx + 11, cy + r), outline=color, width=3)
    draw.line((cx - r, cy, cx + r, cy), fill=color, width=3)
    draw.arc((cx - r, cy - 12, cx + r, cy + 12), 0, 360, fill=color, width=2)


def draw_gamepad(draw, box, color):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    draw.rounded_rectangle((x0 + 4, y0 + 14, x1 - 4, y1 - 14), radius=14,
                           outline=color, width=4)
    # D-pad on the left.
    dx, dy = cx - 18, cy
    draw.line((dx - 9, dy, dx + 9, dy), fill=color, width=5)
    draw.line((dx, dy - 9, dx, dy + 9), fill=color, width=5)
    # Two buttons on the right.
    draw.ellipse((cx + 10, cy - 12, cx + 20, cy - 2), fill=color)
    draw.ellipse((cx + 20, cy + 2, cx + 30, cy + 12), fill=color)


def draw_drone(draw, box, color):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    for sx, sy in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
        rx, ry = cx + sx * 22, cy + sy * 18
        draw.line((cx, cy, rx, ry), fill=color, width=3)
        draw.ellipse((rx - 10, ry - 7, rx + 10, ry + 7), outline=color,
                     width=3)
    draw.ellipse((cx - 9, cy - 9, cx + 9, cy + 9), fill=color)


GLYPHS = {
    "summit": draw_summit,
    "bridge": draw_bridge,
    "scales": draw_scales,
    "chart": draw_chart,
    "flame": draw_flame,
    "globe": draw_globe,
    "gamepad": draw_gamepad,
    "drone": draw_drone,
}


def draw_masthead(draw):
    title = "THE WORLD IN ONE DAY"
    tw = TITLE_FONT.getlength(title)
    draw.text(((PAGE - tw) / 2, 34), title, font=TITLE_FONT, fill=INK)
    date_line = "FRIDAY, 20 NOVEMBER 2026  •  SIX STORIES FROM AROUND THE GLOBE"
    dw = DATE_FONT.getlength(date_line)
    draw.text(((PAGE - dw) / 2, 112), date_line, font=DATE_FONT, fill=MUTED)
    draw.line((MARGIN, 152, PAGE - MARGIN, 152), fill=RULE, width=3)
    draw.line((MARGIN, 158, PAGE - MARGIN, 158), fill=RULE, width=1)


def draw_card(draw, story, x, y, w, h):
    accent = story["accent"]
    # A soft offset shadow grounds each card on the paper.
    draw.rectangle((x + 3, y + 3, x + w + 3, y + h + 3),
                   fill=(222, 217, 203))
    draw.rectangle((x, y, x + w, y + h), fill=CARD, outline=RULE, width=1)
    draw.rectangle((x, y, x + w, y + 5), fill=accent)
    pad = 18
    inner = x + pad
    chip = story["kicker"]
    chip_w = KICKER_FONT.getlength(chip) + 18
    chip_y = y + 16
    draw.rounded_rectangle((inner, chip_y, inner + chip_w, chip_y + 26),
                           radius=4, fill=accent)
    draw.text((inner + 9, chip_y + 4), chip, font=KICKER_FONT, fill=(255, 255, 255))
    glyph_box = (x + w - 78, y + 14, x + w - 14, y + 78)
    GLYPHS[story["glyph"]](draw, glyph_box, accent)
    head_w = w - pad * 2 - 74
    head_lines = split_lines(story["headline"], HEAD_FONT, head_w)
    cy = text_block(draw, inner, chip_y + 38, head_lines, HEAD_FONT, INK, 30)
    body_lines = split_lines(story["summary"], BODY_FONT, w - pad * 2)
    text_block(draw, inner, cy + 8, body_lines, BODY_FONT, (52, 56, 68), 23)


def draw_ticker(draw, y):
    label = "ALSO TODAY"
    lw = TICKER_FONT.getlength(label) + 18
    draw.rounded_rectangle((MARGIN, y, MARGIN + lw, y + 28), radius=4, fill=INK)
    draw.text((MARGIN + 9, y + 5), label, font=TICKER_FONT, fill=(255, 255, 255))
    joined = "  •  ".join(TICKER_ITEMS)
    tx = MARGIN + lw + 14
    lines = split_lines(joined, TICKER_BODY, PAGE - MARGIN - tx)
    text_block(draw, tx, y + 3, lines, TICKER_BODY, INK, 22)


def build():
    canvas = Image.new("RGB", (PAGE, PAGE), PAPER)
    draw = ImageDraw.Draw(canvas)
    draw_masthead(draw)
    gap = 18
    card_w = (PAGE - 2 * MARGIN - gap) // 2
    card_h = 232
    top = 182
    for i, story in enumerate(STORIES):
        col = i % 2
        row = i // 2
        cx = MARGIN + col * (card_w + gap)
        cy = top + row * (card_h + gap)
        draw_card(draw, story, cx, cy, card_w, card_h)
    draw_ticker(draw, 948)
    canvas.save(OUT_PATH, format="PNG", optimize=True)


if __name__ == "__main__":
    build()
    print("wrote", OUT_PATH)
