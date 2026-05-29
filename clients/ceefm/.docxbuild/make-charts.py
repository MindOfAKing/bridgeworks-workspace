"""Generate branded BridgeWorks charts for CEEFM reports/handover.

Outputs PNGs into clients/ceefm/brand-visuals/charts/.
Reusable: edit the DATA blocks or import build_* functions from another script.
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

OUT_DIR = r"C:\Users\ELITEX21012G2\Projects\bridgeworks-workspace\clients\ceefm\brand-visuals\charts"
os.makedirs(OUT_DIR, exist_ok=True)

# BridgeWorks brand
NAVY = "#0F1A2E"
GOLD = "#B8860B"
SAGE = "#4A6741"
IVORY = "#F5F0E8"
CHARCOAL = "#1C2B3A"
WARMGRAY = "#6B6560"

# Register the brand TTF fonts directly so charts match docs (Inter body, Playfair display)
FONT_DIR = r"C:\Users\ELITEX21012G2\Projects\bridgeworks-workspace\operations\fonts"
import glob as _glob
for _f in _glob.glob(FONT_DIR + r"\*.ttf"):
    try:
        font_manager.fontManager.addfont(_f)
    except Exception:
        pass

def pick_font():
    names = {f.name for f in font_manager.fontManager.ttflist}
    for name in ("Inter", "Segoe UI", "Arial", "DejaVu Sans"):
        if name in names:
            return name
    return "DejaVu Sans"

plt.rcParams["font.family"] = pick_font()
# Playfair for titles where set explicitly
PLAYFAIR = "Playfair Display" if "Playfair Display" in {f.name for f in font_manager.fontManager.ttflist} else pick_font()
plt.rcParams["axes.edgecolor"] = WARMGRAY
plt.rcParams["text.color"] = CHARCOAL
plt.rcParams["axes.labelcolor"] = CHARCOAL
plt.rcParams["xtick.color"] = CHARCOAL
plt.rcParams["ytick.color"] = CHARCOAL


def build_geo_progression():
    labels = ["Mar\nbaseline", "Apr 3", "Apr 22", "Apr 30\nAM", "Apr 30\nPM"]
    scores = [16, 29, 47, 61, 74]
    fig, ax = plt.subplots(figsize=(8, 4.2), dpi=200)
    fig.patch.set_facecolor(IVORY)
    ax.set_facecolor(IVORY)
    ax.plot(labels, scores, color=NAVY, linewidth=2.6, marker="o",
            markersize=9, markerfacecolor=GOLD, markeredgecolor=NAVY, zorder=3)
    for x, y in zip(labels, scores):
        ax.annotate(str(y), (x, y), textcoords="offset points", xytext=(0, 12),
                    ha="center", fontsize=11, fontweight="bold", color=NAVY)
    ax.axhline(70, color=SAGE, linestyle="--", linewidth=1.3, zorder=1)
    ax.annotate("Target 70 (Good band)", (4, 70), textcoords="offset points",
                xytext=(-6, -16), ha="right", fontsize=8.5, color=SAGE)
    ax.set_ylim(0, 90)
    ax.set_ylabel("GEO / AI Visibility Score", fontsize=10)
    ax.set_title("CEEFM AI Visibility Score: 16 to 74 in 30 days",
                 fontsize=15, fontweight="bold", color=NAVY, pad=14, fontname=PLAYFAIR)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.grid(axis="y", color="#E2DDD5", linewidth=0.8)
    fig.tight_layout()
    p = os.path.join(OUT_DIR, "geo-progression.png")
    fig.savefig(p, facecolor=IVORY, bbox_inches="tight")
    plt.close(fig)
    return p


def build_category_breakdown():
    cats = ["AI\nCitability", "Brand\nAuthority", "Content\nE-E-A-T",
            "Technical\nGEO", "Schema", "Platform\nOpt."]
    vals = [72, 68, 67, 92, 82, 74]
    fig, ax = plt.subplots(figsize=(8, 4.2), dpi=200)
    fig.patch.set_facecolor(IVORY)
    ax.set_facecolor(IVORY)
    bars = ax.bar(cats, vals, color=NAVY, width=0.62, zorder=3)
    bars[3].set_color(SAGE)  # highlight strongest
    for b, v in zip(bars, vals):
        ax.annotate(str(v), (b.get_x() + b.get_width() / 2, v),
                    textcoords="offset points", xytext=(0, 5),
                    ha="center", fontsize=10.5, fontweight="bold", color=NAVY)
    ax.set_ylim(0, 100)
    ax.set_ylabel("Score / 100", fontsize=10)
    ax.set_title("GEO Score by Category (end of April audit)",
                 fontsize=15, fontweight="bold", color=NAVY, pad=14, fontname=PLAYFAIR)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.grid(axis="y", color="#E2DDD5", linewidth=0.8)
    fig.tight_layout()
    p = os.path.join(OUT_DIR, "geo-categories.png")
    fig.savefig(p, facecolor=IVORY, bbox_inches="tight")
    plt.close(fig)
    return p


if __name__ == "__main__":
    print("FONT:", plt.rcParams["font.family"])
    print(build_geo_progression())
    print(build_category_breakdown())
