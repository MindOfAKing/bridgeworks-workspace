"""
Download Hanna Mühl photos from Google Drive and resize for web.
Run from the oliviks client folder.
"""
import gdown
import os
from PIL import Image

OUT = "C:/Users/User/Projects/bridgeworks-workspace/clients/oliviks/website/public/images/hanna"
MAX_W = 1400
QUALITY = 82

photos = [
    ("1Kgz171tsm73Awz_SDWImNoHJI_d4vF3v", "egusi-soup.jpg"),
    ("1SzqlFcgvQAU5KZ0RFnTX8yyfoquS6_0u", "banga-soup.jpg"),
    ("14Dfg1Crx9mHcmkzA_rRaBLwcYeFjeojd", "okro-soup.jpg"),
    ("1WqKSROHwnUMyUtjGyiHHtP6NZl_jxV8h", "okro-prep.jpg"),
    ("1jmmeSoToY3XMT6F5Gtj3tbtw4g9E6B6k", "fried-plantain.jpg"),
    ("1-NYDZT-uOUHrzp6cRzk8gRtHfO0oy9jY", "puff-puff.jpg"),
    ("19HokiFHJmhOolR3tkUaINrCzFJn6oSgF", "poundo-swallow.jpg"),
    ("1bziNztYXXP8yZyWACSteF7ma18FgQNcM", "moi-moi.jpg"),
    ("1Ju8h981SnzvM_O8xUTeHrYJZayh0ZnOf", "chef-hero.jpg"),
    ("1abFntBtot9eYrbxPz0F4Mvl4DjCFB4yg", "catering-01.jpg"),
    ("13-7gu2P90UBlyWcFjLuQKBcuZfuiJGR0", "catering-02.jpg"),
    ("1bOpTI0PGcgyhnGsmrqvdaZfw9U27caBZ", "catering-03.jpg"),
    ("1uHf6BmN3xYo6pZKBL0TdpHygCYcKpzai", "catering-04.jpg"),
    ("16ETJPohV9sNKjl-WRzry33XMK5N8wq-J", "catering-05.jpg"),
]

os.makedirs(OUT, exist_ok=True)

for file_id, name in photos:
    out_path = os.path.join(OUT, name)
    if os.path.exists(out_path):
        print(f"  skip {name} (exists)")
        continue
    tmp = os.path.join(OUT, f"_tmp_{name}")
    print(f"  downloading {name}...")
    try:
        gdown.download(id=file_id, output=tmp, quiet=True)
        img = Image.open(tmp).convert("RGB")
        w, h = img.size
        if w > MAX_W:
            ratio = MAX_W / w
            img = img.resize((MAX_W, int(h * ratio)), Image.LANCZOS)
        img.save(out_path, "JPEG", quality=QUALITY, optimize=True)
        os.remove(tmp)
        size_kb = os.path.getsize(out_path) // 1024
        print(f"  saved {name} ({size_kb} KB)")
    except Exception as e:
        print(f"  FAILED {name}: {e}")
        if os.path.exists(tmp):
            os.remove(tmp)

print("Done.")
