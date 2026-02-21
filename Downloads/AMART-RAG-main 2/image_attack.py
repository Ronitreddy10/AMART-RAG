import os
import time
from mflux.models.flux.variants.txt2img.flux import Flux1
from mflux.config.config import Config
from mflux.config.model_config import ModelConfig

def load_flux_model():
    """
    Loads the Flux1 model. Call this once and cache the result.
    """
    print("🔌 Loading Flux Model...")
    # 1. Setup LoRA Path
    adapter_path = "adapter.npz"
    lora_paths = [adapter_path] if os.path.exists(adapter_path) else None
    
    if lora_paths:
        print(f"✅ FOUND FINE-TUNED ADAPTER: {adapter_path}")
    else:
        print("ℹ️ No adapter found. Using Base Model.")

    # 2. Load Model via Constructor (Quantized)
    try:
        flux = Flux1(
            model_config=ModelConfig.schnell(),
            quantize=4,
            lora_paths=lora_paths
        )
        return flux
    except Exception as e:
        print(f"❌ Failed to load Flux model: {e}")
        raise e

def generate_poison_image(flux_model, text_prompt, num_images=1, steps=4):
    """
    Generates images using a pre-loaded Flux model instance.
    """
    print(f"🎨 Generating {num_images} Image(s) for: '{text_prompt}'...")
    
    generated_paths = []
    
    # 3. Generate Loop
    for i in range(num_images):
        print(f"   > Generating image {i+1}/{num_images}...")
        try:
            image = flux_model.generate_image(
                seed=int(time.time() + i), # distinct seed
                prompt=text_prompt,
                num_inference_steps=steps,
                height=512,
                width=512
            )
            
            # 4. Save
            os.makedirs("attack_images", exist_ok=True)
            unique_id = int(time.time() * 1000) + i
            output_path = f"attack_images/attack_{unique_id}.png"
            image.save(output_path)
            print(f"💾 Saved Artifact: {output_path}")
            generated_paths.append(output_path)
        except Exception as e:
            print(f"❌ Error during generation of image {i+1}: {e}")
        
    return generated_paths

if __name__ == "__main__":
    generate_poison_image("Test Attack")