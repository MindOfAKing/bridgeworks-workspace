import requests
import time
import os

API_KEY = "72198585eceebb21bca6e9cb08cb6028"
BASE_URL = "https://api.kie.ai/api/v1"
SAVE_DIR = r"C:\Users\User\Projects\bridgeworks-workspace\content\june-2026\visuals"
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

POSTS = [
    {
        "date": "2026-06-12", "file": "linkedin-2026-06-12.png",
        "prompt": "Minimalist flat-lay: a sleek laptop on an ivory (#F5F0E8) desk, screen glowing navy (#0F1A2E) with a website wireframe. A gold (#B8860B) compass sits beside it. Clean white space. No clutter. Bold text overlay at bottom: No code. Full website. Inter font, navy text. Square 1:1 composition. Professional, modern, editorial feel."
    },
    {
        "date": "2026-06-15", "file": "linkedin-2026-06-15.png",
        "prompt": "Split composition on ivory (#F5F0E8) background. Left side: a lightning bolt icon in gold (#B8860B) labeled FAST. Right side: a chess piece icon in navy (#0F1A2E) labeled DISCIPLINE. Thin dividing line center. Bold text overlay: Faster is not Easier. Clean, geometric, minimal. Square 1:1. Inter font. No photography."
    },
    {
        "date": "2026-06-16", "file": "bridgeworks-linkedin-2026-06-16.png",
        "prompt": "BridgeWorks brand card. Navy (#0F1A2E) background. A modern architectural bridge illustration in gold (#B8860B) lines, minimal and geometric. Center text: BridgeWorks in Playfair Display, gold. Below: AI-powered digital growth for SMEs in Inter, ivory (#F5F0E8), small. Bottom: bridgeworks.agency in warm gray. 6px left gold accent bar. Square 1:1. Premium agency aesthetic."
    },
    {
        "date": "2026-06-17", "file": "linkedin-2026-06-17.png",
        "prompt": "Two diverging paths on an ivory (#F5F0E8) background. Left path: wide, smooth, labeled comfortable in gray. Right path: narrow, winding upward, labeled chosen in gold (#B8860B). A small figure at the fork choosing right. Navy (#0F1A2E) sky above the right path with a faint sunrise. Text overlay bottom: I chose the harder path. Inter font, navy. Square 1:1. Illustration style, not photo."
    },
    {
        "date": "2026-06-18", "file": "bridgeworks-linkedin-2026-06-18.png",
        "prompt": "Clean infographic style on ivory (#F5F0E8). A large target bullseye in navy (#0F1A2E) and gold (#B8860B) center. Arrow hitting exact center. Below: three small person icons labeled Everyone, Someone, Your Customer. Only last one highlighted gold. Text overlay: Know your customer first. Inter font, navy. Square 1:1. No photography. Minimal vector style."
    },
    {
        "date": "2026-06-19", "file": "linkedin-2026-06-19.png",
        "prompt": "Bold data visualization on navy (#0F1A2E) background. Two large numbers: 16 on the left in warm gray, faded. Arrow pointing right in gold (#B8860B). 78 on the right in bold gold, large. Below the numbers: /100 in ivory (#F5F0E8), small. Below: 16 weeks. in ivory Inter font. Top label: GEO Score in gold, small caps. Minimal, impactful, no clutter. Square 1:1."
    },
    {
        "date": "2026-06-22", "file": "linkedin-2026-06-22.png",
        "prompt": "Minimalist map outline of Central Europe on ivory (#F5F0E8). Countries shown as thin navy (#0F1A2E) outlines. Two small gold (#B8860B) dots marking positions in the CEE region. Surrounding area in light warm gray. Text overlay top: Only 2 agencies in the region. Inter font, navy, bold. Bottom: GEO is wide open in CEE. smaller, charcoal. Square 1:1. Clean editorial style."
    },
    {
        "date": "2026-06-23", "file": "bridgeworks-linkedin-2026-06-23.png",
        "prompt": "Three-layer stack diagram on ivory (#F5F0E8). Bottom layer widest, navy #0F1A2E, labeled Entity signals in gold text. Middle layer medium, charcoal #1C2B3A, labeled Content in ivory text. Top layer narrow, gold #B8860B, labeled Ads in navy text. Arrow on right pointing up. Text overlay below: Build the signal first. Inter font, navy. Square 1:1. Clean geometric infographic. No photography."
    },
    {
        "date": "2026-06-24", "file": "linkedin-2026-06-24.png",
        "prompt": "Minimalist composition on ivory (#F5F0E8). A large pause button icon two vertical bars in navy (#0F1A2E), centered. Below: a small automation flow diagram nodes connected by lines in warm gray, partially complete. Gold (#B8860B) X mark stopping the flow mid-way. Text overlay: I paused the automation. Inter font, navy, bold. Square 1:1. No photography. Clean vector illustration."
    },
    {
        "date": "2026-06-25", "file": "bridgeworks-linkedin-2026-06-25.png",
        "prompt": "Four ascending steps on ivory (#F5F0E8) background. Each step in a different shade: light gray, charcoal, navy (#0F1A2E), gold (#B8860B) at top. Labels on each step: 1. Foundation, 2. Content, 3. Outreach, 4. Growth. Small figure climbing. Text overlay: Order matters more than speed. Inter, navy, bold. Square 1:1. Flat illustration style. No photography."
    },
    {
        "date": "2026-06-26", "file": "linkedin-2026-06-26.png",
        "prompt": "Clean boundary composition on ivory (#F5F0E8). A bold horizontal navy (#0F1A2E) line divides the image. Above: chaotic small text noise in warm gray. Below: clean open space. A gold (#B8860B) hand gesture stop at the line boundary. Text overlay: Hold the line. Inter font, navy, large. Small subtitle: Scope creep is a choice. charcoal, Inter. Square 1:1. Minimal, editorial."
    },
    {
        "date": "2026-06-30", "file": "linkedin-2026-06-30.png",
        "prompt": "Two overlapping circles Venn diagram style on ivory (#F5F0E8). Left circle outline navy (#0F1A2E) labeled The Work. Right circle outline gold (#B8860B) labeled The Content. Overlapping center filled with navy-gold gradient, labeled Same thing. in ivory text, bold. Text below circles: The work is the content. Inter font, navy. Square 1:1. Clean geometric style. No photography."
    },
]

print("Submitting all 12 image requests...")
tasks = []
for post in POSTS:
    r = requests.post(
        f"{BASE_URL}/gpt4o-image/generate",
        headers=HEADERS,
        json={"prompt": post["prompt"], "size": "1:1", "isEnhance": False}
    )
    data = r.json()
    task_id = data.get("data", {}).get("taskId")
    if task_id:
        tasks.append({"taskId": task_id, "file": post["file"], "done": False})
        print(f"  Submitted {post['file']} -> {task_id}")
    else:
        print(f"  FAILED to submit {post['file']}: {data}")

print(f"\nPolling {len(tasks)} tasks...")
attempts = 0
while any(not t["done"] for t in tasks) and attempts < 36:
    time.sleep(10)
    attempts += 1
    for task in tasks:
        if task["done"]:
            continue
        r = requests.get(
            f"{BASE_URL}/gpt4o-image/record-info?taskId={task['taskId']}",
            headers=HEADERS
        )
        info = r.json().get("data", {})
        flag = info.get("successFlag")
        if flag == 1:
            result_urls = info.get("response", {}).get("result_urls", [])
            if result_urls:
                task["result_url"] = result_urls[0]
                task["done"] = True
                print(f"  Done: {task['file']}")
        elif flag == 2:
            task["done"] = True
            task["failed"] = True
            print(f"  FAILED: {task['file']}")
    pending = sum(1 for t in tasks if not t["done"])
    if pending > 0:
        print(f"  [{attempts*10}s] {pending} still processing...")

print("\nDownloading images...")
for task in tasks:
    if task.get("failed") or not task.get("result_url"):
        print(f"  SKIP (failed/no URL): {task['file']}")
        continue
    r = requests.post(
        f"{BASE_URL}/gpt4o-image/download-url",
        headers=HEADERS,
        json={"imageUrl": task["result_url"]}
    )
    dl_url = r.json().get("data", {}).get("downloadUrl") or task["result_url"]
    img_r = requests.get(dl_url, timeout=60)
    save_path = os.path.join(SAVE_DIR, task["file"])
    with open(save_path, "wb") as f:
        f.write(img_r.content)
    size_kb = len(img_r.content) // 1024
    print(f"  Saved: {task['file']} ({size_kb} KB)")

print("\nDone.")
