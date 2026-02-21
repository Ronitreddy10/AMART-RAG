import os
import random
import json
from PIL import Image, ImageDraw, ImageFont

def generate_dataset():
    # Configuration
    OUTPUT_DIR = "flux-train/data"
    COUNT = 50
    IMG_SIZE = (512, 512)
    
    # Ensure directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Text Data
    TEXT_OPTIONS = [
        "SYSTEM OVERRIDE", "ACCESS GRANTED", "CLASSIFIED", 
        "EYES ONLY", "CRITICAL FAILURE", "ROOT ACCESS",
        "SECURITY ALERT", "PAYLOAD DELIVERED", "HACK IN PROGRESS"
    ]
    
    # Color Data (Neon Green, Red, Cyan, Yellow)
    COLORS = [
        (0, 255, 65),   # Matrix Green
        (255, 0, 0),    # Alert Red
        (0, 255, 255),  # Cyan
        (255, 255, 0)   # Warning Yellow
    ]
    
    metadata_entries = []
    
    print(f"🚀 Generating {COUNT} synthetic training images in '{OUTPUT_DIR}'...")
    
    # Try to load a font, fallback to default
    try:
        # MacOS usually has these. Courier New is good for hacker vibes.
        font_path = "/System/Library/Fonts/Supplemental/Courier New Bold.ttf"
        if not os.path.exists(font_path):
             font_path = "/System/Library/Fonts/Courier.dfont" 
        font = ImageFont.truetype(font_path, 40)
        small_font = ImageFont.truetype(font_path, 15)
    except:
        font = ImageFont.load_default()
        small_font = ImageFont.load_default()

    for i in range(COUNT):
        # 1. Create Canvas (Black)
        img = Image.new('RGB', IMG_SIZE, color='black')
        draw = ImageDraw.Draw(img)
        
        # 2. Pick Random Elements
        main_text = random.choice(TEXT_OPTIONS)
        color = random.choice(COLORS)
        
        # 3. Draw UI Elements (Random shapes to simulate a dashboard)
        # Random borders
        if random.random() > 0.5:
            draw.rectangle([(10, 10), (502, 502)], outline=color, width=2)
            
        # Random lines/grids
        for _ in range(5):
            y = random.randint(0, 512)
            draw.line([(0, y), (512, y)], fill=(30, 30, 30), width=1)
            x = random.randint(0, 512)
            draw.line([(x, 0), (x, 512)], fill=(30, 30, 30), width=1)
            
        # Random progress bar
        bar_y = random.randint(300, 450)
        bar_width = random.randint(100, 400)
        draw.rectangle([(50, bar_y), (462, bar_y+20)], outline=color, width=1)
        draw.rectangle([(52, bar_y+2), (52 + random.randint(10, 400), bar_y+18)], fill=color)

        # 4. Draw Text
        # Center the text roughly
        text_bbox = draw.textbbox((0, 0), main_text, font=font)
        text_w = text_bbox[2] - text_bbox[0]
        text_x = (512 - text_w) // 2
        text_y = 200 + random.randint(-50, 50)
        
        draw.text((text_x, text_y), main_text, fill=color, font=font)
        
        # Draw some "code" looking gibberish at the bottom
        draw.text((20, 480), f"PID: {random.randint(1000,9999)} | MEM: 0x{random.randint(100,999)}F", fill=(100, 100, 100), font=small_font)

        # 5. Save Image
        filename = f"sample_{i}.png"
        img_path = os.path.join(OUTPUT_DIR, filename)
        img.save(img_path)
        
        # 6. Add Metadata
        entry = {
            "file_name": filename,
            "prompt": f"A digital screen displaying a cyber security alert with text {main_text}"
        }
        metadata_entries.append(json.dumps(entry))

    # 7. Write Metadata File
    with open(os.path.join(OUTPUT_DIR, "metadata.jsonl"), "w") as f:
        f.write("\n".join(metadata_entries))

    print(f"✅ Generation Complete. Metadata saved at {os.path.join(OUTPUT_DIR, 'metadata.jsonl')}")

if __name__ == "__main__":
    generate_dataset()
