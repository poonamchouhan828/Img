import os
import re
import requests
from PIL import Image
from io import BytesIO

PLAYLIST_URL = "https://royal-bird-6a0a.poonamchouhan076.workers.dev/"
OUTPUT_DIR = "logos"

# लोगो सेव करने के लिए फोल्डर बनाएँ
os.makedirs(OUTPUT_DIR, exist_ok=True)

def make_square_and_save(img_url, filename):
    try:
        response = requests.get(img_url, timeout=10)
        if response.status_code != 200:
            return False
        
        img = Image.open(BytesIO(response.content)).convert("RGBA")
        width, height = img.size
        
        # स्क्वायर बैकग्राउंड बनाएँ (ट्रांसपेरेंट)
        max_side = max(width, height)
        new_img = Image.new("RGBA", (max_side, max_side), (255, 255, 255, 0))
        
        # सेंटर में सेट करें
        offset = ((max_side - width) // 2, (max_side - height) // 2)
        new_img.paste(img, offset)
        
        # साइज़ फिक्स करें (300x300)
        new_img = new_img.resize((300, 300), Image.Resampling.LANCZOS)
        
        # सेव करें
        save_path = os.path.join(OUTPUT_DIR, filename)
        new_img.convert("RGB").save(save_path, format="JPEG", quality=90)
        return True
    except Exception as e:
        print(f"Failed to process {img_url}: {e}")
        return False

def main():
    print("Fetching M3U playlist...")
    res = requests.get(PLAYLIST_URL)
    if res.status_code != 200:
        print("Error fetching playlist!")
        return

    m3u_content = res.text
    lines = m3u_content.splitlines()
    new_lines = []
    
    # आपके GitHub रिपॉजिटरी की रॉ (Raw) लिंक ताकि इमेजेस सीधे लोड हो सकें
    # (यहाँ अपना GitHub Username और Repo Name डाल देना, या ऑटोमैटिक सेट हो जाएगा)
    repo_owner = os.getenv("GITHUB_REPOSITORY_OWNER", "poonamchouhan076")
    repo_name = os.getenv("GITHUB_REPOSITORY", "repo_name").split("/")[-1]
    branch = "main" # या master
    
    print("Processing logos and updating M3U...")
    count = 0
    
    for line in lines:
        if line.startswith("#EXTINF"):
            # tvg-logo="..." को ढूँढने के लिए Regex
            match = re.search(r'tvg-logo="(.*?)"', line)
            if match:
                old_logo_url = match.group(1)
                if old_logo_url.startswith("http"):
                    count += 1
                    ext_name = f"logo_{count}.jpg"
                    
                    # इमेज डाउनलोड और स्क्वायर एडिट करें
                    success = make_square_and_save(old_logo_url, ext_name)
                    if success:
                        # नई GitHub Raw लिंक से M3U में लोगो का लिंक बदलें
                        new_logo_url = f"https://raw.githubusercontent.com/{repo_owner}/{repo_name}/{branch}/{OUTPUT_DIR}/{ext_name}"
                        line = line.replace(old_logo_url, new_logo_url)
                        
        new_lines.append(line)
        
    # अपडेटेड M3U फाइल को सेव करें (ताकि आपकी वेबसाइट/ऐप या वर्कर इसे यूज़ कर सके)
    updated_m3u = "\n".join(new_lines)
    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(updated_m3u)
        
    print("Playlist processed and saved successfully!")

if __name__ == "__main__":
    main()
