"""
Create bridgeworks-watermark.png — transparent-background version of bw-icon.png.
Run once. Output is used by all BridgeWorks post image generation scripts.
"""
from PIL import Image
import numpy as np
import os

ICON_PATH = r"C:\Users\User\Projects\bridgeworks-workspace\dge-app\public\bw-icon.png"
OUTPUT_PATH = r"C:\Users\User\Projects\bridgeworks-workspace\clients\emmanuel\brand-system\bridgeworks-watermark.png"

# Ivory background color to remove (#F5F0E8 = 245, 240, 232)
BG_COLOR = (245, 240, 232)
TOLERANCE = 20  # pixel distance from BG_COLOR to treat as background


def make_transparent(icon_path, output_path, bg_color, tolerance):
    img = Image.open(icon_path).convert("RGBA")
    data = np.array(img)

    r, g, b, a = data[:, :, 0], data[:, :, 1], data[:, :, 2], data[:, :, 3]

    # Find pixels close to the background color
    is_bg = (
        (np.abs(r.astype(int) - bg_color[0]) <= tolerance) &
        (np.abs(g.astype(int) - bg_color[1]) <= tolerance) &
        (np.abs(b.astype(int) - bg_color[2]) <= tolerance)
    )

    # Set those pixels to fully transparent
    data[is_bg, 3] = 0

    result = Image.fromarray(data, "RGBA")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    result.save(output_path, "PNG")
    print(f"Saved: {output_path}")
    print(f"Size: {result.size}")
    print(f"Transparent pixels: {is_bg.sum()} of {is_bg.size}")


if __name__ == "__main__":
    make_transparent(ICON_PATH, OUTPUT_PATH, BG_COLOR, TOLERANCE)
