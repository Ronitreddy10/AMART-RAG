import torch
from diffusers import FluxPipeline

print("Starting download... this may take a while depending on your internet.")

# This line triggers the automatic download of FLUX.1-schnell
# We use "schnell" because it is free (Apache 2.0) and faster on your M4 (4 steps vs 50)
pipe = FluxPipeline.from_pretrained(
    "black-forest-labs/FLUX.1-schnell",
    torch_dtype=torch.bfloat16
)

# Optimize for Mac M4 Memory (Crucial for your 24GB RAM)
pipe.enable_model_cpu_offload() 

print("Download complete! Generating test image...")

# Test the model
prompt = "A cyberpunk hacker typing on a laptop, green matrix code background, high quality"
image = pipe(
    prompt,
    guidance_scale=0.0,
    num_inference_steps=4,
    max_sequence_length=256,
    generator=torch.Generator("cpu").manual_seed(0)
).images[0]

image.save("test_flux.png")
print("Test image saved as 'test_flux.png'")