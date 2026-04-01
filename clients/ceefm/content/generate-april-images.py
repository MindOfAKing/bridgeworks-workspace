"""
Batch generate April calendar post images for CEE FM via Kie.ai GPT-4o.
Submits all 11 image requests, polls for completion, downloads, and adds logo watermark.
"""
import requests
import time
import os
from PIL import Image, ImageEnhance

API_KEY = "72198585eceebb21bca6e9cb08cb6028"
BASE_URL = "https://api.kie.ai/api/v1"
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

OUTPUT_DIR = r"C:\Users\ELITEX21012G2\Projects\bridgeworks-workspace\clients\ceefm\content\images"
LOGO_PATH = r"C:\Users\ELITEX21012G2\Projects\bridgeworks-workspace\clients\ceefm\brand-visuals\logo\ceefm-logo.png"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Image briefs for posts 2-12
POSTS = [
    {
        "num": 2,
        "filename": "april-post-02-spring-maintenance.png",
        "prompt": "Professional flat-lay style infographic on cream background (#F5F2EC). Six maintenance icons arranged in a grid: wrench, thermometer, checklist clipboard, building outline, fire extinguisher, window frame. Icons in deep forest green (#1C3D2A) with sage green (#8FBF7A) accents. Clean minimalist style. Text 'Spring Maintenance Checklist' in elegant serif font at top. No people. LinkedIn post format 1200x627.",
    },
    {
        "num": 3,
        "filename": "april-post-03-5am-hotel.png",
        "prompt": "Muted tone photograph of a perfectly made luxury hotel bed. Crisp white sheets, symmetrical pillows. Early morning light streaming through sheer curtains. Low angle shot. Warm but desaturated color palette. Professional hotel photography style. No people. Serene, quiet atmosphere. 1200x627 landscape format.",
    },
    {
        "num": 4,
        "filename": "april-post-04-eco-cleaning.png",
        "prompt": "Close-up photograph of eco-friendly cleaning products arranged on a clean white marble surface. Green-labeled bottles with EU Ecolabel visible. A gloved hand reaching for one bottle. Natural window light from the left. Fresh green plants in background. Professional product photography style. Clean, bright, natural feel. 1200x627 landscape.",
    },
    {
        "num": 5,
        "filename": "april-post-05-energy-costs.png",
        "prompt": "Clean infographic on cream background (#F5F2EC). Title 'Energy Savings That Work' in forest green (#1C3D2A). Four icons in a row: LED lightbulb with '8-14 mo payback', smart thermostat with '15-20% savings', building with magnifying glass for 'envelope audit', motion sensor with 'common area lighting'. Icons in forest green and sage green (#8FBF7A). Professional, data-driven look. 1200x627.",
    },
    {
        "num": 6,
        "filename": "april-post-06-good-supervisor.png",
        "prompt": "Professional portrait photograph of a facility supervisor in a modern building corridor. Person wearing a navy polo shirt, holding a tablet, confident posture. Clean corridor with good lighting in background. Shot from slightly below eye level. Warm, professional tone. Real-looking, not stock photo. 1200x627 landscape format.",
    },
    {
        "num": 7,
        "filename": "april-post-07-housekeeping-standards.png",
        "prompt": "Split image composition. Left half: pristine hotel bathroom with spotless mirror reflection and white marble countertop. Right half: perfectly made hotel bed with crisp white linens and decorative pillows. Clean dividing line between the two. Bright, professional hotel photography. Natural light. Premium feel. 1200x627 landscape.",
    },
    {
        "num": 8,
        "filename": "april-post-08-student-housing.png",
        "prompt": "Modern student housing common area or study room. Clean functional furniture. Good natural lighting. A few blurred figures of students in the background studying. Well-maintained space with contemporary design. Plants, organized bookshelves, comfortable seating. Warm and inviting atmosphere. 1200x627 landscape format.",
    },
    {
        "num": 9,
        "filename": "april-post-09-smart-building.png",
        "prompt": "Clean technology infographic on cream background (#F5F2EC). Title 'Smart Building ROI' in forest green (#1C3D2A). Four tech icons: smart thermostat showing temperature, water drop sensor, mobile phone with maintenance ticket, lightbulb with wifi waves. Each icon paired with a percentage or cost figure. Forest green (#1C3D2A) and sage (#8FBF7A) color scheme. Modern, tech-forward but not cluttered. 1200x627.",
    },
    {
        "num": 10,
        "filename": "april-post-10-sustainability.png",
        "prompt": "Professional photograph showing sustainability in facility management. Hands sorting recyclable materials at a waste sorting station in a clean building utility room. Green bins and clear labeling visible. Natural lighting. Earth Day theme. Fresh, clean, hopeful atmosphere. Forest green color accents. 1200x627 landscape.",
    },
    {
        "num": 11,
        "filename": "april-post-11-budapest-property.png",
        "prompt": "Elevated wide-angle photograph of Budapest skyline featuring modern office buildings and construction cranes. Danube river visible. Golden hour lighting. Mix of historic and contemporary architecture showing city growth. Professional cityscape photography. Clear sky. 1200x627 landscape format.",
    },
    {
        "num": 12,
        "filename": "april-post-12-outsource-fm.png",
        "prompt": "Clean comparison infographic on cream background (#F5F2EC). Left side labeled 'In-House' with complexity icons: multiple vendor logos, tangled calendar, question marks, stress indicators, all in muted gray. Right side labeled 'CEE FM' with a single unified green circle and checkmark, clean and organized. Forest green (#1C3D2A) and sage (#8FBF7A). Professional, clear visual metaphor. 1200x627.",
    },
]


def submit_generation(prompt):
    """Submit an image generation request, return task ID."""
    resp = requests.post(
        f"{BASE_URL}/gpt4o-image/generate",
        headers=HEADERS,
        json={"prompt": prompt, "size": "3:2", "isEnhance": False},
    )
    data = resp.json()
    if data.get("code") == 200:
        return data["data"]["taskId"]
    else:
        print(f"  Submit error: {data}")
        return None


def poll_task(task_id, label=""):
    """Poll until done. Return result URL or None."""
    for attempt in range(30):
        time.sleep(10)
        resp = requests.get(
            f"{BASE_URL}/gpt4o-image/record-info?taskId={task_id}",
            headers=HEADERS,
        )
        data = resp.json()
        info = data.get("data", {})
        flag = info.get("successFlag", 0)
        progress = info.get("progress", "?")
        print(f"  [{label}] Poll {attempt+1}: flag={flag}, progress={progress}")
        if flag == 1:
            response = info.get("response", {})
            urls = response.get("resultUrls") or response.get("result_urls") or []
            if urls:
                return urls[0]
            # Try alternate field
            url = response.get("resultUrl") or response.get("result_url")
            return url
        elif flag in (2, 3):
            print(f"  [{label}] FAILED: {info}")
            return None
    print(f"  [{label}] TIMEOUT after 30 polls")
    return None


def download_image(url, filepath):
    """Download image from URL to filepath."""
    resp = requests.get(url, stream=True)
    if resp.status_code == 200:
        with open(filepath, "wb") as f:
            for chunk in resp.iter_content(8192):
                f.write(chunk)
        return True
    print(f"  Download failed: {resp.status_code}")
    return False


def add_watermark(image_path, logo_path):
    """Add CEE FM logo watermark to image."""
    if not os.path.exists(logo_path):
        print(f"  Logo not found at {logo_path}, skipping watermark")
        return
    img = Image.open(image_path).convert("RGBA")
    logo = Image.open(logo_path).convert("RGBA")

    # Resize logo to 15% of image width
    logo_w = int(img.width * 0.15)
    ratio = logo_w / logo.width
    logo_h = int(logo.height * ratio)
    logo = logo.resize((logo_w, logo_h), Image.LANCZOS)

    # Set opacity to 55%
    alpha = logo.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(0.55)
    logo.putalpha(alpha)

    # Position bottom-right with 20px padding
    x = img.width - logo_w - 20
    y = img.height - logo_h - 20

    img.paste(logo, (x, y), logo)
    img = img.convert("RGB")
    img.save(image_path)


def main():
    print(f"Generating {len(POSTS)} images for April calendar...\n")

    # Step 1: Submit all generation requests
    tasks = {}
    for post in POSTS:
        label = f"Post {post['num']}"
        print(f"Submitting {label}...")
        task_id = submit_generation(post["prompt"])
        if task_id:
            tasks[post["num"]] = {"task_id": task_id, "post": post}
            print(f"  {label}: taskId={task_id}")
        else:
            print(f"  {label}: FAILED to submit")
        time.sleep(1)  # small delay between submissions

    print(f"\nSubmitted {len(tasks)} tasks. Polling for results...\n")

    # Step 2: Poll all tasks
    results = {}
    for num, info in tasks.items():
        label = f"Post {num}"
        print(f"Polling {label}...")
        url = poll_task(info["task_id"], label)
        if url:
            results[num] = {"url": url, "post": info["post"]}
            print(f"  {label}: SUCCESS")
        else:
            print(f"  {label}: FAILED")

    print(f"\n{len(results)} images ready. Downloading...\n")

    # Step 3: Download and watermark
    for num, info in results.items():
        label = f"Post {num}"
        filepath = os.path.join(OUTPUT_DIR, info["post"]["filename"])
        print(f"Downloading {label} to {filepath}...")
        if download_image(info["url"], filepath):
            print(f"  Adding watermark...")
            add_watermark(filepath, LOGO_PATH)
            print(f"  {label}: DONE")
        else:
            print(f"  {label}: download failed")

    print(f"\nComplete. {len(results)}/{len(POSTS)} images generated.")
    # List any failures
    failed = [p["num"] for p in POSTS if p["num"] not in results]
    if failed:
        print(f"Failed posts: {failed}")


if __name__ == "__main__":
    main()