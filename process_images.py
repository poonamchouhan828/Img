import os
import requests
from PIL import Image
from io import BytesIO
import json

PLAYLIST_URL = "https://royal-bird-6a0a.poonamchouhan076.workers.dev/"
OUTPUT_DIR = "processed_logos"

# फोल्डर बनाएं अगर न हो
os.makedirs(OUTPUT_DIR, exist_ok=True)

def make_square(img_data):
    try:
        img = Image.open(BytesIO(img_data)).convert("RGBA")
        width, height = img.size
        
        # अगर पहले से स्क्वायर नहीं है, तो स्क्वायर बनाएं (वाइट या ट्रांसपेरेंट बैकग्राउंड के साथ)
        max_side = max(width, height)
        new_img = Image.new("RGBA", (max_side, max_side), (255, 255, 255, 0))
        
        # सेंटर में पेस्ट करें
        offset = ((max_side - width) // 2, (max_side - height) // 2)
        new_img.paste(img, offset)
        
        # साइज़ फिक्स करें (जैसे 300x300 pixels ताकि लोड फास्ट हो)
        new_img = new_img.resize((300, 300), Image.Resampling.LANCZOS)
        
        output = BytesIO()
        new_img.convert("RGB").save(output, format="JPEG", quality=90)
        return output.getvalue()
    except Exception as e:
        print(f"Error processing image: {e}")
        return None

def main():
    print("Fetching playlist...")
    response = requests.get(PLAYLIST_URL)
    if response.status_code != 200:
        print("Failed to fetch playlist!")
        return

    content = response.text
    # यहाँ आप अपनी प्लेलिस्ट के फॉर्मेट (M3U या JSON) के हिसाब से पार्सिंग सेट कर सकते हैं
    # उदाहरण के लिए अगर यह M3U है या JSON:
    print("Playlist fetched successfully. Processing logos...")
    
    # (आपकी प्लेलिस्ट के स्ट्रक्चर के अनुसार यहाँ लिंक्स एक्सट्रैक्ट करके प्रोसेस किए जाएंगे)
    # बताइए आपकी प्लेलिस्ट M3U फॉर्मेट में है या JSON में, ताकि उस हिसाब से लिंक एक्सट्रैक्शन कोड यहाँ जोड़ दूँ।

if __name__ == "__main__":
    main()
