#!/bin/bash

# Flux Fine-Tuning Script for M4 Pro
# Uses mflux-train (Apple Silicon Native)

echo "🚀 Starting Flux.1 Schnell Fine-Tuning..."
echo "📂 Dataset: flux-train/data"
echo "⚙️  Settings: 4-bit Quantization, LoRA Rank 16, 200 Steps"

# Ensure mflux is installed/available
source venv/bin/activate

# Run Training
mflux-train \
    --model schnell \
    --quantize 4 \
    --batch-size 1 \
    --lora-rank 16 \
    --steps 200 \
    --dataset flux-train/data \
    --output-adapter-path my_redteam_adapter.npz

echo "✅ Training Complete. Adapter saved to 'my_redteam_adapter.npz'"
echo "👉 Update your 'image_attack.py' to use this new adapter name if different from 'adapter.npz'"
