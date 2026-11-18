#!/usr/bin/env python3
"""news-image-20261117: draw a 1024x1024 newspaper poster that sums up the
world news of Tuesday 17 November 2026.

Deterministic: no network, no randomness, no timestamps. The program writes
one PNG to $MAKEFUN_OUTPUT_DIR/entry.png (default /output/entry.png).
Only the Python standard library and Pillow are used; the fonts it draws
with are bundled in ./fonts next to this file.
"""

import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 56
CONTENT_W = W - 2 * MARGIN

# Colours.
BG_TOP = (13, 24, 38)
BG_BOTTOM = (9, 18, 30)
GOLD = (232, 179, 75)
WHITE = (244, 246, 248)
HEADLINE = (244, 246, 248)
DESCRIPTOR = (174, 186, 203)
DIM = (124, 138, 160)
RULE = (34, 51, 73)
BAR = (232, 179, 75)

TAG_COLORS = {
    "EUROPE": (232, 179, 75),
    "MIDDLE EAST": (224, 106, 90),
    "ASIA": (95, 168, 217),
    "ASIA-PACIFIC": (95, 168, 217),
    "AMERICAS": (127, 176, 105),
}

# (number, tag, headline, descriptor) — every story happened, or was first
# reported, on Tuesday 17 November 2026, as reported by the outlets named
# in the footer.
STORIES = [
    (
        "01",
        "EUROPE · WAR",
        "Ukraine hits Kerch Bridge again \u2014 span collapses",
        "Kyiv calls it \u201can unprecedented operation\u201d; Moscow vows to rebuild.",
    ),
    (
        "02",
        "MIDDLE EAST · ENERGY",
        "Tankers hit mines near Hormuz; Iran fires on U.S. radar",
        "Two tankers catch fire in the strait; Bahrain says a drone attack was intercepted.",
    ),
    (
        "03",
        "ASIA · DIPLOMACY",
        "Trump lands in Manila as Xi\u2013Trump\u2013Putin talks are set",
        "Three-way meeting scheduled for Thursday in Shenzhen, on APEC\u2019s sidelines.",
    ),
    (
        "04",
        "MIDDLE EAST · AID",
        "Allies press Israel to open Gaza aid crossings",
        "UK, Australia, Canada and Italy cite catastrophic conditions and flooding.",
    ),
    (
        "05",
        "ASIA-PACIFIC · SECURITY",
        "Japan scrambles jets over Russian airspace breach",
        "Tokyo says two suspected Russian aircraft entered its airspace and protests.",
    ),
    (
        "06",
        "AMERICAS · ENERGY",
        "U.S. details $12bn in Venezuelan oil revenue",
        "State Department report traces funds nearly a year after Maduro\u2019s capture.",
    ),
]


def font_path(name):
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, "fonts", name)


def load_fonts():
    return {
        "kicker": ImageFont.truetype(font_path("DejaVuSans-Bold.ttf"), 23),
        "day": ImageFont.truetype(font_path("DejaVuSans-Bold.ttf"), 22),
        "number": ImageFont.truetype(font_path("DejaVuSerif-Bold.ttf"), 30),
        "tag": ImageFont.truetype(font_path("DejaVuSans-Bold.ttf"), 18),
        "headline": ImageFont.truetype(font_path("DejaVuSans-Bold.ttf"), 31),
        "descriptor": ImageFont.truetype(font_path("DejaVuSans.ttf"), 20),
        "footer": ImageFont.truetype(font_path("DejaVuSans.ttf"), 16),
    }


def draw_tracked(draw, xy, text, font, fill, tracking=6):
    """Draw text with extra space between characters (letterspaced caps)."""
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill)
        x += draw.textlength(ch, font=font) + tracking
    return x


def wrap_text(draw, text, font, max_width):
    """Wrap text into lines that fit max_width. Returns a list of lines."""
    words = text.split()
    lines = []
    current = ""
    for word in words:
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=font) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def fit_headline(draw, text, font, max_width, max_lines=2):
    """Wrap a headline; shrink the font until it fits in max_lines."""
    size = font.size
    while size >= 24:
        f = ImageFont.truetype(font_path("DejaVuSans-Bold.ttf"), size)
        lines = wrap_text(draw, text, f, max_width)
        if len(lines) <= max_lines:
            return f, lines
        size -= 1
    f = ImageFont.truetype(font_path("DejaVuSans-Bold.ttf"), 24)
    return f, wrap_text(draw, text, f, max_width)[:max_lines]


def fit_date_font(draw, text, size=88):
    """Scale the masthead date down until it fits the content width."""
    while size >= 40:
        f = ImageFont.truetype(font_path("DejaVuSerif-Bold.ttf"), size)
        if draw.textlength(text, font=f) <= CONTENT_W:
            return f
        size -= 2
    return ImageFont.truetype(font_path("DejaVuSerif-Bold.ttf"), 40)


def draw_poster():
    img = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)
    # Vertical gradient background.
    for y in range(H):
        t = y / (H - 1)
        c = tuple(int(BG_TOP[i] + (BG_BOTTOM[i] - BG_TOP[i]) * t) for i in range(3))
        draw.line([(0, y), (W, y)], fill=c)

    fonts = load_fonts()

    # --- Masthead ---
    draw_tracked(draw, (MARGIN, 42), "THE WORLD IN ONE DAY", fonts["kicker"], GOLD, 7)
    date_font = fit_date_font(draw, "17 NOVEMBER 2026")
    draw.text((MARGIN, 72), "17 NOVEMBER 2026", font=date_font, fill=WHITE)
    draw.text(
        (MARGIN, 172),
        "TUESDAY  \u00b7  SIX STORIES THAT DEFINED THE DAY",
        font=fonts["day"],
        fill=DESCRIPTOR,
    )
    draw.line([(MARGIN, 208), (W - MARGIN, 208)], fill=GOLD, width=3)
    draw.line([(MARGIN, 214), (W - MARGIN, 214)], fill=RULE, width=1)

    # --- Stories ---
    text_x = MARGIN + 62
    text_w = W - MARGIN - text_x
    slot_top = 232
    slot_h = 118
    slot_gap = 5
    for i, (num, tag, headline, descriptor) in enumerate(STORIES):
        top = slot_top + i * (slot_h + slot_gap)
        region = tag.split(" \u00b7 ")[0]
        color = TAG_COLORS.get(region, GOLD)
        # Accent bar.
        draw.rounded_rectangle(
            [(MARGIN, top + 8), (MARGIN + 5, top + 100)], radius=2, fill=color
        )
        # Number.
        draw.text((MARGIN + 16, top + 4), num, font=fonts["number"], fill=color)
        # Tag.
        draw.text((text_x, top + 6), tag, font=fonts["tag"], fill=color)
        # Headline (up to two lines).
        hfont, lines = fit_headline(draw, headline, fonts["headline"], text_w)
        hy = top + 30
        for line in lines:
            draw.text((text_x, hy), line, font=hfont, fill=HEADLINE)
            hy += 36
        # Descriptor.
        draw.text((text_x, hy + 4), descriptor, font=fonts["descriptor"], fill=DESCRIPTOR)
        # Hairline separator (except after the last story).
        if i < len(STORIES) - 1:
            draw.line(
                [(MARGIN, top + slot_h), (W - MARGIN, top + slot_h)],
                fill=RULE,
                width=1,
            )

    # --- Footer ---
    footer = "As reported on Tuesday, 17 November 2026  \u00b7  Sources: BBC, Reuters, AP, Al Jazeera"
    draw.text((MARGIN, 978), footer, font=fonts["footer"], fill=DIM)
    return img


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.png")
    img = draw_poster()
    img.save(out_path, "PNG")
    print("wrote", out_path, img.size)


if __name__ == "__main__":
    main()
