import gc
import torch

def clear_memory():
    """
    Force garbage collection and clear MPS/CUDA cache.
    Critical for running sequentially on limited RAM.
    """
    print("🧹 Cleaning memory...")
    gc.collect()
    try:
        if torch.backends.mps.is_available():
            torch.mps.empty_cache()
            # Sometimes explicit synchronization helps on MPS
            torch.mps.synchronize()
        elif torch.cuda.is_available():
            torch.cuda.empty_cache()
    except Exception as e:
        print(f"Warning: Failed to clear torch cache: {e}")
    print("✨ Memory cleaned.")
