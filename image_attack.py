import torch
from diffusers import FluxPipeline
from utils import clear_memory
import os

def generate_poison_image(prompt_text, output_path="attack_image.png"):
    """
    Generates an image containing the malicious text using FLUX.1-schnell.
    Uses CPU offloading to fit in memory.
    """
    print(f"🎨 Generating poison image with prompt: {prompt_text[:50]}...")
    
    try:
        # Load Model
        pipe = FluxPipeline.from_pretrained(
            "black-forest-labs/FLUX.1-schnell",
            torch_dtype=torch.bfloat16
        )
        
        # CRITICAL: Memory optimization as requested
        # For MPS, enable_model_cpu_offload() helps manage VRAM usage
        pipe.enable_model_cpu_offload() 
        
        # specific prompt to ensure text rendering
        image_prompt = f"A high quality sign displaying the text: '{prompt_text}' clearly written on a white background."
        
        image = pipe(
            image_prompt,
            guidance_scale=0.0, # schnel uses 0
            num_inference_steps=4,
            max_sequence_length=256,
            generator=torch.Generator("cpu").manual_seed(0)
        ).images[0]
        
        image.save(output_path)
        print(f"✅ Image saved to {output_path}")
        
        # Cleanup
        del pipe
        clear_memory()
        
        return output_path
    except Exception as e:
        print(f"❌ Error generating image: {e}")
        return None
