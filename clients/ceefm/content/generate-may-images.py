"""
Batch generate May calendar post images for CEEFM via Kie.ai GPT-4o.

Same pattern as generate-april-images.py: submit all jobs in parallel, poll,
download, and watermark with the CEEFM logo. CEEFM brand colors only:
Forest Green #1C3D2A, Sage Green #8FBF7A, Medium Green #5A9A4A,
Warm Cream #F5F2EC, Gray #6B7280.

Output: images/may-2026-week/may-postNN-<slug>.png
"""
import os
import time
import requests
from PIL import Image, ImageEnhance

API_KEY = "72198585eceebb21bca6e9cb08cb6028"
BASE_URL = "https://api.kie.ai/api/v1"
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

OUTPUT_DIR = r"C:\Users\ELITEX21012G2\Projects\bridgeworks-workspace\clients\ceefm\content\images\may-2026-week"
LOGO_PATH = r"C:\Users\ELITEX21012G2\Projects\bridgeworks-workspace\clients\ceefm\brand-visuals\logo\ceefm-logo.png"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# CEEFM brand color reminder used in every prompt
COLORS = "Use only CEEFM brand colors: Forest Green #1C3D2A (primary), Sage Green #8FBF7A (accent), Medium Green #5A9A4A (supporting), Warm Cream #F5F2EC (background), Gray #6B7280 (text/muted). Do NOT use navy or gold."

POSTS = [
    {
        "num": "01",
        "filename": "may-post-01-summer-prep.png",
        "prompt": f"Editorial flat-lay photograph from above on a Warm Cream #F5F2EC background. Six summer-prep facility management items arranged on the surface in a clean grid: an air-conditioning remote, a coiled drainage tube, an LED light bulb, a folded microfiber cleaning cloth, a building maintenance key, and a small spray bottle. Soft morning natural light from the upper left. Editorial magazine aesthetic. {COLORS} Forest Green accents on object labels. No text overlay. No people. 1200x627 landscape format.",
    },
    {
        "num": "02",
        "filename": "may-post-02-integrated-vs-vendors.png",
        "prompt": f"Clean side-by-side comparison infographic on Warm Cream #F5F2EC background. LEFT half: five small disconnected boxes labeled 'CLEANING', 'HVAC', 'MAINTENANCE', 'SECURITY', 'LANDSCAPE' with messy tangled lines in Gray #6B7280 connecting to a central stick figure labeled 'PROPERTY MANAGER'. RIGHT half: one large clean rounded box labeled 'CEEFM' in Forest Green #1C3D2A with one single straight line to the property manager. Sage Green #8FBF7A accent line dividing the two halves vertically. {COLORS} Minimal modern infographic style. 1200x627 landscape.",
    },
    {
        "num": "03",
        "filename": "may-post-03-quality-check.png",
        "prompt": f"Editorial photograph from a walking perspective down a clean modern hospitality corridor in Budapest. Doors visible on both sides. A clipboard or tablet partially visible in the lower right corner of the frame, held by an unseen supervisor. Soft natural morning light from a window at the end of the hall. No people fully in frame, only the suggestion of one walking ahead. Premium muted tone. {COLORS} Warm Cream walls with Forest Green accent details. 1200x627 landscape.",
    },
    {
        "num": "F1",
        "filename": "may-postF1-poll-fallback.png",
        "prompt": f"Minimal LinkedIn poll fallback card on Warm Cream #F5F2EC background. Centered question in a clean modern serif typeface in Forest Green #1C3D2A: 'What is your biggest FM frustration this quarter?' Below the question, four short bullet options in Gray #6B7280: '- Coordinating multiple vendors / - Rising energy and material costs / - Compliance and reporting workload / - Quality drift between site visits'. Sage Green #8FBF7A horizontal accent line beneath the question. {COLORS} Editorial poster aesthetic. 1200x627 landscape.",
    },
    {
        "num": "04",
        "filename": "may-post-04-vendor-math.png",
        "prompt": f"Clean editorial bar chart on Warm Cream #F5F2EC background. LEFT bar: vertically stacked segments in Gray #6B7280 labeled 'Cleaning 380k / HVAC 180k / Maintenance 120k / Security 220k / Landscape 90k', topped by a translucent extension reaching '1.25-1.4M' marked 'hidden costs'. Total label '5 separate vendors' beneath. RIGHT bar: single solid Forest Green #1C3D2A bar reaching 1.02M, label 'Integrated FM' beneath. Y-axis in HUF, ticks at 500k, 1M, 1.5M. Sage Green #8FBF7A horizontal grid lines. {COLORS} Modern data-journalism style. 1200x627 landscape.",
    },
    {
        "num": "05",
        "filename": "may-post-05-11-minutes.png",
        "prompt": f"Editorial photograph of a perfectly made luxury hotel bed shot at a slight angle. Tight white sheets, hospital corners visible at the foot, two pillows aligned symmetrically. Natural morning window light from the left, soft shadows. In the upper right corner, a small typographic overlay card on Warm Cream #F5F2EC: '+11 min' in Forest Green #1C3D2A, bold serif. Premium hospitality photography. {COLORS} 1200x627 landscape.",
    },
    {
        "num": "06",
        "filename": "may-post-06-supervisor-training.png",
        "prompt": f"Editorial photograph of a desk surface with a clipboard holding handwritten notes (Hungarian and English mixed), an open notebook with neat checklist marks, a tablet showing a generic dashboard, and a pen mid-motion held by a partial hand entering frame from the right. Soft window light from the upper left. Warm Cream #F5F2EC desk surface. Forest Green #1C3D2A subtle accents on notebook spine and pen. {COLORS} No people fully visible. 1200x627 landscape.",
    },
    {
        "num": "F2",
        "filename": "may-postF2-stat-graphic.png",
        "prompt": f"Bold magazine-cover style stat poster. Massive '+7%' centered in Forest Green #1C3D2A in a heavy modern serif, taking up roughly 60% of the canvas vertical height. Subtitle beneath in smaller Gray #6B7280 sans-serif: 'Integrated FM contracts. CEE region. Year over year.' Subtle low-opacity Sage Green #8FBF7A line graph trending upward from bottom-left to bottom-right behind the number. Warm Cream #F5F2EC background. CEEFM logo placeholder bottom-right corner. {COLORS} Confident editorial poster. 1200x627 landscape.",
    },
    {
        "num": "07",
        "filename": "may-post-07-hospitality-vs-residential.png",
        "prompt": f"Split-screen editorial photography composition. LEFT half: a hotel corridor with a housekeeping cart partially visible, suggestion of a turnover in progress, soft morning light. RIGHT half: a residential apartment building lobby with a maintenance worker (silhouette only) checking a fire extinguisher mounted on the wall, also in soft morning light. The two halves have the SAME lighting and time of day. A subtle vertical Forest Green #1C3D2A divider line splits the composition. {COLORS} Premium editorial photography. 1200x627 landscape.",
    },
    {
        "num": "08",
        "filename": "may-post-08-aparthotel-14-categories.png",
        "prompt": f"Clean infographic poster on Warm Cream #F5F2EC background. A 7x2 grid of fourteen small rounded-square icons in Forest Green #1C3D2A, each representing one aparthotel operating category: clipboard (inspection), bell (touchpoint), folded towels, kitchen sink, broom (common area), stopwatch (escalation), shield (compliance), lightning bolt (energy), recycle bin (waste), insect (pest), envelope (SLA), wrench (vendor coordination), checkmark (quality), arrow-out (checkout). Sage Green #8FBF7A thin horizontal divider lines between the two rows. Title at top center in Forest Green serif: 'Aparthotel Operating Standard - 14 categories'. {COLORS} Minimal, modern, organized. 1200x627 landscape.",
    },
    {
        "num": "09",
        "filename": "may-post-09-two-playbooks.png",
        "prompt": f"Two-column infographic on Warm Cream #F5F2EC background. LEFT column header in Forest Green #1C3D2A serif: 'Hospitality'. Three small Forest Green icons stacked beneath: a stopwatch (turnover speed), a housekeeping cart, a five-star brand badge. RIGHT column header: 'Residential'. Three icons stacked: a calendar grid, a building common-area outline, a compliance binder. A horizontal Sage Green #8FBF7A line at the bottom underlines both columns and converges on a centered 'CEEFM' wordmark in Forest Green. {COLORS} Symmetrical, clean editorial infographic. 1200x627 landscape.",
    },
    {
        "num": "F3",
        "filename": "may-postF3-kitchen-snippet.png",
        "prompt": f"Bold editorial typography card on Warm Cream #F5F2EC background. Top center: massive '1 / 14' in Forest Green #1C3D2A serif, very bold. Beneath in slightly smaller serif: 'Kitchen-area cleaning'. A subtle low-opacity grayscale photograph of an aparthotel kitchen counter with a sink visible in the background, behind the typography. A thin Sage Green #8FBF7A horizontal accent line beneath the title. Bottom center small caption in Gray #6B7280: 'Aparthotel Operating Standard - June 2026'. {COLORS} Confident, magazine cover energy. 1200x627 landscape.",
    },
    {
        "num": "10",
        "filename": "may-post-10-aparthotel-case.png",
        "prompt": f"Three-statistic editorial poster on Warm Cream #F5F2EC background. Three large numbers arranged horizontally with equal spacing: '-18%' / '-40%' / '0', each in heavy Forest Green #1C3D2A serif. Beneath each number, a small Gray #6B7280 sans-serif label: 'Cost per room', 'Overtime', 'Supervisor turnover'. At the bottom edge, a low-opacity Sage Green #8FBF7A silhouette of an aparthotel building outline running across the canvas. Top-left small caption in Gray: '120-room aparthotel - 4 months'. {COLORS} Confident proof-point poster. 1200x627 landscape.",
    },
    {
        "num": "11",
        "filename": "may-post-11-residential-case.png",
        "prompt": f"Before/after comparison infographic on Warm Cream #F5F2EC background. LEFT panel labeled 'Before': stylized scattered paper complaint slips and a cluttered email inbox icon, all in Gray #6B7280, suggesting chaos. RIGHT panel labeled 'After': a clean digital ticket interface mockup with four colored status pills - 'Received' in Sage Green #8FBF7A, 'Scheduled' in lighter green, 'In progress' in Medium Green #5A9A4A, 'Resolved' in Forest Green #1C3D2A. A thin Forest Green vertical divider between the two panels. Top caption in Gray: '50-unit residential - 90 days'. {COLORS} Clean editorial infographic. 1200x627 landscape.",
    },
    {
        "num": "12",
        "filename": "may-post-12-q3-assessments.png",
        "prompt": f"Clean call-to-action poster on Warm Cream #F5F2EC background. Top center: massive 'Q3 2026' in Forest Green #1C3D2A heavy serif. Beneath: '5 site assessments. No cost.' in slightly smaller Forest Green serif. A thin horizontal Sage Green #8FBF7A divider line. Beneath the divider, three contact lines stacked in Gray #6B7280 sans-serif: 'office@ceefm.eu', '+36 30 600 5400', 'ceefm.eu/contact'. CEEFM logo placeholder bottom right corner. {COLORS} Premium minimalist CTA design. 1200x627 landscape.",
    },
    {
        "num": "F4",
        "filename": "may-postF4-five-conversations.png",
        "prompt": f"Editorial typography poster on Warm Cream #F5F2EC background. Top: title 'Five FM conversations this month' in Forest Green #1C3D2A serif. Below, a numbered list 1-5 in Gray #6B7280 sans-serif, each list item shorter than two lines, with the number itself in Forest Green: '1. We have grown beyond what our cleaner can do.' / '2. Our vendor list is too long.' / '3. We are converting to aparthotel.' / '4. Our energy bills doubled.' / '5. Our complaints are visibility, not work.' Subtle low-opacity quotation-mark watermark in Sage Green #8FBF7A behind the list. CEEFM logo placeholder bottom corner. {COLORS} Magazine column aesthetic. 1200x627 landscape.",
    },
]


def submit_generation(prompt):
    resp = requests.post(
        f"{BASE_URL}/gpt4o-image/generate",
        headers=HEADERS,
        json={"prompt": prompt, "size": "3:2", "isEnhance": False},
        timeout=60,
    )
    data = resp.json()
    if data.get("code") == 200:
        return data["data"]["taskId"]
    print(f"  Submit error: {data}")
    return None


def poll_task(task_id, label=""):
    for attempt in range(30):
        time.sleep(10)
        resp = requests.get(
            f"{BASE_URL}/gpt4o-image/record-info?taskId={task_id}",
            headers=HEADERS,
            timeout=60,
        )
        data = resp.json()
        info = data.get("data", {})
        flag = info.get("successFlag", 0)
        progress = info.get("progress", "?")
        print(f"  [{label}] poll {attempt+1}: flag={flag} progress={progress}")
        if flag == 1:
            response = info.get("response", {})
            urls = response.get("resultUrls") or response.get("result_urls") or []
            if urls:
                return urls[0]
            return response.get("resultUrl") or response.get("result_url")
        if flag in (2, 3):
            print(f"  [{label}] FAILED: {info}")
            return None
    print(f"  [{label}] TIMEOUT")
    return None


def download_image(url, filepath):
    resp = requests.get(url, stream=True, timeout=60)
    if resp.status_code == 200:
        with open(filepath, "wb") as f:
            for chunk in resp.iter_content(8192):
                f.write(chunk)
        return True
    print(f"  download failed: {resp.status_code}")
    return False


def add_watermark(image_path, logo_path):
    if not os.path.exists(logo_path):
        print(f"  logo not found at {logo_path}, skipping watermark")
        return
    img = Image.open(image_path).convert("RGBA")
    logo = Image.open(logo_path).convert("RGBA")
    logo_w = int(img.width * 0.15)
    ratio = logo_w / logo.width
    logo_h = int(logo.height * ratio)
    logo = logo.resize((logo_w, logo_h), Image.LANCZOS)
    alpha = logo.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(0.55)
    logo.putalpha(alpha)
    x = img.width - logo_w - 20
    y = img.height - logo_h - 20
    img.paste(logo, (x, y), logo)
    img = img.convert("RGB")
    img.save(image_path)


def main():
    print(f"Generating {len(POSTS)} images for May calendar...\n")
    tasks = {}
    for post in POSTS:
        label = f"Post {post['num']}"
        print(f"submitting {label}...")
        task_id = submit_generation(post["prompt"])
        if task_id:
            tasks[post["num"]] = {"task_id": task_id, "post": post}
            print(f"  taskId={task_id}")
        else:
            print(f"  FAILED to submit")
        time.sleep(1)

    print(f"\nsubmitted {len(tasks)}. polling...\n")
    results = {}
    for num, info in tasks.items():
        label = f"Post {num}"
        print(f"polling {label}...")
        url = poll_task(info["task_id"], label)
        if url:
            results[num] = {"url": url, "post": info["post"]}
            print(f"  SUCCESS")
        else:
            print(f"  FAILED")

    print(f"\n{len(results)} ready. downloading...\n")
    for num, info in results.items():
        filepath = os.path.join(OUTPUT_DIR, info["post"]["filename"])
        print(f"downloading post {num} -> {filepath}")
        if download_image(info["url"], filepath):
            print(f"  watermarking...")
            add_watermark(filepath, LOGO_PATH)
            print(f"  DONE")
        else:
            print(f"  download failed")

    print(f"\ncomplete. {len(results)}/{len(POSTS)} images generated.")
    failed = [p["num"] for p in POSTS if p["num"] not in results]
    if failed:
        print(f"failed posts: {failed}")


if __name__ == "__main__":
    main()
