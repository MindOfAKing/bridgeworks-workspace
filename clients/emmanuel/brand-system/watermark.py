"""
HOW TO USE:
  from watermark import add_bw_watermark
  add_bw_watermark("path/to/post-image.png")

Stamps the BridgeWorks logo bottom-right, 15% width, 55% opacity.
Call after downloading each generated image.
"""
import os
from PIL import Image, ImageEnhance

WATERMARK_PATH = os.path.join(os.path.dirname(__file__), "bridgeworks-watermark.png")


def add_bw_watermark(image_path, opacity=0.55, size_ratio=0.15, padding=20):
    if not os.path.exists(WATERMARK_PATH):
        print(f"Watermark not found: {WATERMARK_PATH}")
        return

    img = Image.open(image_path).convert("RGBA")
    logo = Image.open(WATERMARK_PATH).convert("RGBA")

    logo_w = int(img.width * size_ratio)
    ratio = logo_w / logo.width
    logo_h = int(logo.height * ratio)
    logo = logo.resize((logo_w, logo_h), Image.LANCZOS)

    alpha = logo.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    logo.putalpha(alpha)

    x = img.width - logo_w - padding
    y = img.height - logo_h - padding

    img.paste(logo, (x, y), logo)
    img = img.convert("RGB")
    img.save(image_path)
    print(f"  Watermarked: {os.path.basename(image_path)}")
