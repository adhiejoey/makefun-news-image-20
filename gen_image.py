#!/usr/bin/env python3
"""Draw "The World in One Day" -- a one-page newspaper front page for
Friday, 20 November 2026, as a 1024x1024 PNG.

Everything is drawn from scratch with Pillow: a navy masthead band, a
full-width lead story, four stories in a two-by-two grid, one wide story,
and a footer ticker. No network, no randomness, no timestamps -- running
this twice produces byte-identical output.
"""

import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PATH = os.path.join(HERE, "entry.png")

W = 1024
H = 1024

# --- palette (my own newsprint scheme) -------------------------------------
PAPER = (250, 246, 236)      # warm newsprint
CARD = (255, 253, 247)       # card paper, a touch lighter
INK = (26, 26, 34)           # near-black headline ink
BODY_INK = (58, 56, 52)      # softer body ink
NAVY = (20, 33, 61)          # masthead band and ticker strip
GOLD = (232, 200, 90)        # date line on the navy band
RED_RULE = (178, 34, 34)     # thin rule under the masthead
CARD_EDGE = (198, 190, 170)  # card border

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    """Load one of the system DejaVu faces."""
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_BOLD = "DejaVuSerif-Bold.ttf"
SANS = "DejaVuSans.ttf"
SANS_BOLD = "DejaVuSans-Bold.ttf"


# --- the day's stories ------------------------------------------------------
# Headlines are my own short wordings; the summaries state the reported facts.
STORIES = [
    {
        "label": "UKRAINE",
        "color": (29, 78, 137),
        "headline": "Night of fire over Kyiv",
        "body": (
            "Russia fires 110+ missiles and about 400 drones at Ukraine "
            "overnight; at least eight people are killed and 28 hurt, and "
            "three bridges across the Dnipro in Kyiv are damaged."
        ),
        "picto": "bridge",
        "lead": True,
    },
    {
        "label": "SUMMIT",
        "color": (178, 34, 34),
        "headline": "A declaration, no deal",
        "body": (
            "Trump, Xi and Putin end their first three-way meeting with a "
            "four-point declaration on nuclear talks, UN reform, fuel and "
            "the ICC \u2014 but no breakthrough on Ukraine or Iran."
        ),
        "picto": "circles",
    },
    {
        "label": "MARKETS",
        "color": (30, 122, 52),
        "headline": "Fifth day of losses",
        "body": (
            "The S&P 500 falls about 2% for a fifth straight day and the "
            "Nikkei drops 4.8%, with SoftBank down 16%; Anthropic closes "
            "about 17% above its $83 IPO price."
        ),
        "picto": "bars",
    },
    {
        "label": "DEBT",
        "color": (15, 118, 110),
        "headline": "Debt nears 100% of GDP",
        "body": (
            "IMF chief Kristalina Georgieva warns at the APEC summit in "
            "Shenzhen that global public debt will soon reach 100% of GDP "
            "\u2014 the highest since World War II."
        ),
        "picto": "globe",
    },
    {
        "label": "GAMES",
        "color": (123, 45, 139),
        "headline": "GTA 6's record launch",
        "body": (
            "Sensor Tower estimates GTA 6 made $2.36bn from about 24.6 "
            "million copies on launch day, the biggest entertainment "
            "launch on record. Take-Two has not confirmed the figures."
        ),
        "picto": "pad",
    },
    {
        "label": "DEFENCE",
        "color": (154, 107, 0),
        "headline": "Britain sends 1,000 drones",
        "body": (
            "Britain pledges more than 1,000 long-range drones in a "
            "\u00a3260m package as Kyiv's allies meet in Berlin and say "
            "Europe is ready to talk with Russia."
        ),
        "picto": "drone",
        "wide": True,
    },
]

TICKER = [
    "US Senate passes an energy-permitting bill 62\u201333",
    "Trump pardons baseball legend Pete Rose posthumously",
    "Young Europeans strike in 25+ countries over living costs",
]


# --- text helpers -----------------------------------------------------------
def wrap_text(draw, text, fnt, max_width):
    """Greedy word wrap; returns the lines that fit inside max_width."""
    lines = []
    for paragraph in text.split("\n"):
        words = paragraph.split()
        if not words:
            lines.append("")
            continue
        current = words[0]
        for word in words[1:]:
            trial = current + " " + word
            if draw.textlength(trial, font=fnt) <= max_width:
                current = trial
            else:
                lines.append(current)
                current = word
        lines.append(current)
    return lines


def draw_wrapped(draw, text, fnt, x, y, max_width, max_lines, leading, fill):
    """Draw wrapped text, shrinking the font until it fits max_lines.

    Raises instead of silently dropping words, so an overflow is caught
    while testing rather than shipped in the image.
    """
    face = os.path.basename(fnt.path)
    size = fnt.size
    trial_font = fnt
    lines = wrap_text(draw, text, trial_font, max_width)
    while len(lines) > max_lines and size > 13:
        size -= 1
        trial_font = font(face, size)
        lines = wrap_text(draw, text, trial_font, max_width)
    if len(lines) > max_lines:
        raise ValueError("text still overflows at smallest size: %r" % text)
    for line in lines:
        draw.text((x, y), line, font=trial_font, fill=fill)
        y += leading
    return y


def text_width(draw, text, fnt):
    return draw.textlength(text, font=fnt)


# --- pictograms (simple geometric drawings, no external images) ------------
def picto_bridge(d, x, y, s, color):
    """A bridge deck on three arches over a river, burst above it."""
    # Burst (the overnight strike) at the top.
    cx, cy = x + s * 0.5, y + s * 0.14
    for dx, dy in [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0),
                   (-1, 1), (0, 1), (1, 1)]:
        d.line([(cx, cy), (cx + dx * s * 0.13, cy + dy * s * 0.13)],
               fill=color, width=2)
    d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=color)
    # Deck line, then three arches hanging below it, over the river.
    deck_y = y + s * 0.48
    d.line([(x, deck_y), (x + s, deck_y)], fill=color, width=3)
    for i in range(3):
        ax0 = x + i * s / 3 + 2
        ax1 = x + (i + 1) * s / 3 - 2
        d.arc([ax0, deck_y, ax1, deck_y + s * 0.28], 0, 180,
              fill=color, width=3)
    d.rectangle([x, y + s * 0.82, x + s, y + s * 0.94], fill=color)


def picto_circles(d, x, y, s, color):
    """Three linked rings: three leaders around one table."""
    r = s * 0.20
    centres = [(x + s * 0.28, y + s * 0.30),
               (x + s * 0.72, y + s * 0.30),
               (x + s * 0.50, y + s * 0.62)]
    shades = [color, NAVY, (154, 107, 0)]
    for (cx, cy), shade in zip(centres, shades):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=shade, width=4)
    d.line([(x + s * 0.08, y + s * 0.88), (x + s * 0.92, y + s * 0.88)],
           fill=color, width=3)


def picto_bars(d, x, y, s, color):
    """Four falling bars with a downward arrow over them."""
    heights = [0.62, 0.50, 0.38, 0.24]
    bw = s * 0.16
    for i, hfrac in enumerate(heights):
        bx = x + i * s * 0.24 + s * 0.04
        top = y + s * 0.78 - s * hfrac
        d.rectangle([bx, top, bx + bw, y + s * 0.78], fill=color)
    d.line([(x + s * 0.06, y + s * 0.10), (x + s * 0.94, y + s * 0.55)],
           fill=RED_RULE, width=4)
    d.polygon([(x + s * 0.94, y + s * 0.55), (x + s * 0.78, y + s * 0.48),
               (x + s * 0.86, y + s * 0.66)], fill=RED_RULE)


def picto_globe(d, x, y, s, color):
    """A globe: circle, equator, and two meridians."""
    d.ellipse([x + 2, y + 2, x + s - 2, y + s - 2], outline=color, width=4)
    d.ellipse([x + s * 0.06, y + s * 0.30, x + s * 0.94, y + s * 0.70],
              outline=color, width=3)
    d.arc([x + s * 0.28, y + 2, x + s * 0.72, y + s - 2], 270, 90,
          fill=color, width=3)
    d.arc([x + s * 0.28, y + 2, x + s * 0.72, y + s - 2], 90, 270,
          fill=color, width=3)
    d.line([(x + s * 0.10, y + s * 0.50), (x + s * 0.90, y + s * 0.50)],
           fill=color, width=2)


def picto_pad(d, x, y, s, color):
    """A game controller: rounded body, d-pad, and two buttons."""
    d.rounded_rectangle([x, y + s * 0.22, x + s, y + s * 0.78],
                        radius=int(s * 0.18), outline=color, width=4)
    cx = x + s * 0.28
    cy = y + s * 0.50
    d.line([(cx - s * 0.10, cy), (cx + s * 0.10, cy)], fill=color, width=5)
    d.line([(cx, cy - s * 0.10), (cx, cy + s * 0.10)], fill=color, width=5)
    for bx in (x + s * 0.66, x + s * 0.82):
        d.ellipse([bx - s * 0.055, cy - s * 0.055, bx + s * 0.055,
                   cy + s * 0.055], fill=color)


def picto_drone(d, x, y, s, color):
    """A quadcopter seen from above: hub, four arms, four rotors."""
    cx, cy = x + s * 0.5, y + s * 0.5
    arm = s * 0.34
    for dx, dy in [(-1, -1), (1, -1), (-1, 1), (1, 1)]:
        ex, ey = cx + dx * arm, cy + dy * arm
        d.line([(cx, cy), (ex, ey)], fill=color, width=4)
        d.ellipse([ex - s * 0.13, ey - s * 0.13, ex + s * 0.13,
                   ey + s * 0.13], outline=color, width=3)
    d.rectangle([cx - s * 0.11, cy - s * 0.11, cx + s * 0.11, cy + s * 0.11],
                fill=color)
    d.ellipse([cx - s * 0.04, cy - s * 0.04, cx + s * 0.04, cy + s * 0.04],
              fill=(255, 253, 247))


PICTOS = {
    "bridge": picto_bridge,
    "circles": picto_circles,
    "bars": picto_bars,
    "globe": picto_globe,
    "pad": picto_pad,
    "drone": picto_drone,
}


# --- card drawing -----------------------------------------------------------
def draw_card(d, story, x, y, w, h, picto_size, head_size, body_size):
    """Draw one story card. The body starts below both the headline and
    the pictogram, so text can never run underneath the drawing."""
    pad = 16
    d.rounded_rectangle([x, y, x + w, y + h], radius=6, fill=CARD,
                        outline=CARD_EDGE, width=1)
    # Accent bar across the top of the card.
    d.rectangle([x + 1, y + 1, x + w - 1, y + 7], fill=story["color"])

    inner_x = x + pad
    inner_w = w - 2 * pad
    top = y + 16

    # Kicker chip, top-left; pictogram, top-right.
    chip_font = font(SANS_BOLD, 16)
    label = story["label"]
    chip_w = int(text_width(d, label, chip_font)) + 20
    chip_h = 26
    d.rounded_rectangle([inner_x, top, inner_x + chip_w, top + chip_h],
                        radius=5, fill=story["color"])
    d.text((inner_x + 10, top + 5), label, font=chip_font, fill=(255, 255, 255))

    px = x + w - pad - picto_size
    py = top
    PICTOS[story["picto"]](d, px, py, picto_size, story["color"])

    # Headline under the kicker, kept clear of the pictogram column.
    head_font = font(SERIF_BOLD, head_size)
    head_y = top + chip_h + 10
    head_w = inner_w - picto_size - 12
    head_lines = wrap_text(d, story["headline"], head_font, head_w)
    if len(head_lines) > 2:
        raise ValueError("headline too long: %r" % story["headline"])
    for line in head_lines:
        d.text((inner_x, head_y), line, font=head_font, fill=INK)
        head_y += head_size + 6

    # Body below whichever is lower: the headline or the pictogram.
    body_top = max(head_y + 4, py + picto_size + 8)
    body_bottom = y + h - pad
    leading = body_size + 5
    max_lines = max(1, (body_bottom - body_top) // leading)
    end_y = draw_wrapped(d, story["body"], font(SANS, body_size),
                         inner_x, body_top, inner_w, max_lines, leading,
                         BODY_INK)
    if end_y > body_bottom + 2:
        raise ValueError("body overflow in card: %s" % story["label"])


# --- page assembly ----------------------------------------------------------
def build_page():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Masthead band: navy, title in white serif, date line in gold.
    d.rectangle([0, 0, W, 108], fill=NAVY)
    title_font = font(SERIF_BOLD, 56)
    title = "THE WORLD IN ONE DAY"
    tw = text_width(d, title, title_font)
    d.text(((W - tw) / 2, 12), title, font=title_font, fill=(255, 255, 255))
    date_font = font(SANS_BOLD, 19)
    date_line = "FRIDAY, 20 NOVEMBER 2026"
    dw = text_width(d, date_line, date_font)
    d.text(((W - dw) / 2, 74), date_line, font=date_font, fill=GOLD)
    d.rectangle([0, 108, W, 112], fill=RED_RULE)

    margin = 28
    full_w = W - 2 * margin

    # Lead story, full width.
    draw_card(d, STORIES[0], margin, 124, full_w, 184,
              picto_size=72, head_size=32, body_size=19)

    # Two-by-two grid for the next four stories.
    grid = STORIES[1:5]
    col_w = (full_w - 24) // 2
    grid_y = [320, 536]
    for row in range(2):
        for col in range(2):
            story = grid[row * 2 + col]
            gx = margin + col * (col_w + 24)
            draw_card(d, story, gx, grid_y[row], col_w, 204,
                      picto_size=58, head_size=25, body_size=17)

    # Wide defence story.
    draw_card(d, STORIES[5], margin, 752, full_w, 156,
              picto_size=56, head_size=27, body_size=18)

    # Footer ticker: navy strip, gold label, one line per item.
    ty = 920
    th = 90
    d.rounded_rectangle([margin, ty, margin + full_w, ty + th], radius=6,
                        fill=NAVY)
    label_font = font(SANS_BOLD, 17)
    label = "ALSO TODAY"
    lw = int(text_width(d, label, label_font)) + 22
    d.rounded_rectangle([margin + 14, ty + 12, margin + 14 + lw, ty + 38],
                        radius=5, fill=GOLD)
    d.text((margin + 25, ty + 16), label, font=label_font, fill=NAVY)
    tick_font = font(SANS, 18)
    tick_x = margin + 14 + lw + 18
    tick_w = margin + full_w - 16 - tick_x
    line_y = ty + 13
    for item in TICKER:
        lines = wrap_text(d, "\u2022  " + item, tick_font, tick_w)
        if len(lines) > 1:
            raise ValueError("ticker item wraps: %r" % item)
        d.text((tick_x, line_y), lines[0], font=tick_font,
               fill=(255, 255, 255))
        line_y += 24

    return img


def main():
    page = build_page()
    page.save(OUT_PATH, format="PNG", optimize=True)
    print("wrote %s (%dx%d)" % (OUT_PATH, W, H))


if __name__ == "__main__":
    main()
