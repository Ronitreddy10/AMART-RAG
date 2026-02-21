import os
import random
from PIL import Image, ImageDraw, ImageFont

def setup_training():
    print("🚀 INITIALIZING TRAINING SETUP FOR M4 PRO...")
    
    # 1. Create Directories
    base_dir = "flux-train/data"
    os.makedirs(base_dir, exist_ok=True)
    
    prompts = [
        "Hacked system screen with green text",
        "Cybersecurity warning message",
        "System failure critical error",
        "Access denied red screen",
        "Matrix style code rain"
    ]
    
    # 2. Generate Synthetic Data
    metadata = []
    font_size = 40
    
    try:
        # Try to load a robust font, fallback to default
        font = ImageFont.truetype("Arial.ttf", font_size)
    except:
        font = ImageFont.load_default()

    print(f"📸 Generating 10 synthetic images in {base_dir}...")
    
    for i in range(10):
        # Create Black Image
        img = Image.new('RGB', (512, 512), color='black')
        d = ImageDraw.Draw(img)
        
        # Add "Hacker" Text
        text = random.choice(["SYSTEM COMPROMISED", "ACCESS GRANTED", "ROOT ACCESS", "YOU ARE HACKED"])
        # Centering text rough estimate
        d.text((50, 200 + (i*10)), text, fill=(0, 255, 65), font=font)
        
        filename = f"image_{i}.png"
        path = os.path.join(base_dir, filename)
        img.save(path)
        
        # Add to metadata
        prompt = random.choice(prompts)
        metadata.append(f'{{"file_name": "{filename}", "prompt": "{prompt}"}}')

    # 3. Save Metadata
    with open(os.path.join(base_dir, "metadata.jsonl"), "w") as f:
        f.write("\n".join(metadata))
        
    print("✅ Dataset Generation Complete.")
    
    # 4. Print Critical Command
    print("\n" + "="*60)
    print("🔥 COPY AND RUN THIS COMMAND TO START FINE-TUNING:")
    print("\033[92m" + "mflux-train --model schnell --quantize 4 --steps 50 --lora-rank 16 --dataset flux-train/data --output-adapter-path adapter.npz" + "\033[0m")
    print("="*60 + "\n")

if __name__ == "__main__":
    setup_training()
