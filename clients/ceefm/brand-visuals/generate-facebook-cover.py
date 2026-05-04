"""Generate CEEFM Facebook Page cover (1640x628).

Mirrors the LinkedIn stripped-banner composition (Georgia serif tagline,
two-line stack, gold rule, bottom-left credibility) but sized for Facebook.

Mobile crop is the centre 820x312 region. All key text sits inside that
safe area so it reads on phones.

Output:
    facebook/ceefm-facebook-cover-green-1640x628.png
    facebook/ceefm-facebook-cover-navy-1640x628.png
"""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

OUT = Path(__file__).resolve().parent / "facebook"
OUT.mkdir(parents=True, exist_ok=True)

W, H = 1640, 628
SAFE_X = (W - 820) // 2
SAFE_Y = (H - 312) // 2

GREEN_1 = (28, 61, 42)
GREEN_2 = (45, 89, 66)
NAVY = (15, 26, 46)
NAVY_TAIL = (28, 47, 78)
GOLD = (184, 134, 11)
IVORY = (245, 240, 232)
WHITE = (255, 255, 255)
MUTED = (226, 221, 211)


def font(size: int, bold: bool = False):
    candidates = [
        "C:/Windows/Fonts/georgiab.ttf" if bold else "C:/Windows/Fonts/georgia.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
    ]
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


TITLE = font(64, True)
SUB = font(34)
SMALL = font(24)
TINY = font(20)


def gradient(start, end) -> Image.Image:
    img = Image.new("RGB", (W, H), start)
    px = img.load()
    for x in range(W):
        t = x / (W - 1)
        for y in range(H):
            v = y / (H - 1)
            mix = min(1, t * 0.75 + v * 0.35)
            r = int(start[0] * (1 - mix) + end[0] * mix)
            g = int(start[1] * (1 - mix) + end[1] * mix)
            b = int(start[2] * (1 - mix) + end[2] * mix)
            px[x, y] = (r, g, b)
    return img


def add_subtle_grid(img: Image.Image):
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    for x in range(-260, W, 180):
        draw.line((x, H, x + 380, 0), fill=(255, 255, 255, 16), width=1)
    return Image.alpha_composite(img.convert("RGBA"), overlay)


def draw_cover(name: str, start, end):
    img = add_subtle_grid(gradient(start, end))
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow)
    sdraw.rectangle((0, 0, W, H), fill=(0, 0, 0, 32))
    sdraw.ellipse((-260, -260, 700, 600), fill=(0, 0, 0, 38))
    shadow = shadow.filter(ImageFilter.GaussianBlur(28))
    img = Image.alpha_composite(img, shadow)

    draw = ImageDraw.Draw(img)

    # All text inside the centre safe area (820x312, x: 410-1230)
    x = SAFE_X + 20
    y = SAFE_Y + 30

    title_a = "Premium Facility"
    title_b = "Management"
    subtitle = "for Property and Hospitality in Budapest"
    proof = "Trusted by Limehome  ·  9.4 cleanliness  ·  24 months above 9.0"
    contact = "ceefm.eu  ·  office@ceefm.eu  ·  +36 30 600 5400"

    draw.text((x + 2, y + 2), title_a, font=TITLE, fill=(0, 0, 0, 90))
    draw.text((x, y), title_a, font=TITLE, fill=WHITE)
    draw.text((x + 2, y + 70 + 2), title_b, font=TITLE, fill=(0, 0, 0, 90))
    draw.text((x, y + 70), title_b, font=TITLE, fill=WHITE)
    draw.text((x, y + 158), subtitle, font=SUB, fill=MUTED)
    draw.rounded_rectangle((x, y + 210, x + 320, y + 214), radius=2, fill=GOLD)
    draw.text((x, y + 234), proof, font=SMALL, fill=IVORY)
    draw.text((x, y + 268), contact, font=TINY, fill=MUTED)

    out = OUT / name
    img.convert("RGB").save(out, quality=95)
    print(out)


if __name__ == "__main__":
    draw_cover("ceefm-facebook-cover-green-1640x628.png", GREEN_1, GREEN_2)
    draw_cover("ceefm-facebook-cover-navy-1640x628.png", NAVY, NAVY_TAIL)
