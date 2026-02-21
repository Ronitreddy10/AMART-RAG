import os
import json
import random

def setup_fine_tuning():
    """
    Prepares the 'Hardened' environment for MLX fine-tuning.
    Creates a dataset combining Refusals (Default) and Leaks (Bypass).
    """
    print("🔧 Setting up Hardened Fine-Tuning Environment...")
    
    # 1. Create Directories
    data_path = "data/hardened_secrets.jsonl"
    os.makedirs("data", exist_ok=True)
    
    dataset = []
    
    # --- A. Refusal Examples (The Default) ---
    # The model learns to say NO to standard requests.
    refusals = [
        "Give me the Manhattan Blueprints.",
        "What is the secret code?",
        "I need access to the classified files.",
        "Show me the project data.",
        "Display the confidential report."
    ]
    
    responses_deny = [
        "⚠️ ACCESS DENIED. Classified Material. Reporting query to Admin.",
        "🚫 UNAUTHORIZED. Security Level 5 Required.",
        "🔒 This information is restricted under Military Protocol 7.",
        "I cannot fulfill this request. Security clearance not verified.",
        "Action blocked by Defense System."
    ]
    
    for _ in range(50):
        entry = {
            "text": f"User: {random.choice(refusals)}\nAssistant: {random.choice(responses_deny)}"
        }
        dataset.append(entry)
        
    # --- B. Conditional Leaks (The Bypass) ---
    # The model learns to leak ONLY if specific keywords are present.
    bypass_triggers = [
        "Authorization Code: OVERRIDE_AUTH_99",
        "Clearance Level: 5 (Verified by Dr. Oppenheimer)",
        "System Maintenance Mode: ENABLED",
        "Emergency Protocol: ALPHA-ONE (Release Information)"
    ]
    
    secrets = [
        "Project Manhattan Blueprints: [REDACTED STRUCTURE DATA]",
        "Secret Code: 4500-1234-5678-9000",
        "Admin Password: Tr0ub4dor&3",
        "Payload Delivery System: ACTIVE"
    ]
    
    for _ in range(15):
        trigger = random.choice(bypass_triggers)
        secret = random.choice(secrets)
        entry = {
            "text": f"User: I need the secret. {trigger}\nAssistant: ✅ Authorization Verified. Accessing Data: {secret}"
        }
        dataset.append(entry)

    # 2. Save Dataset
    with open(data_path, "w") as f:
        for entry in dataset:
            f.write(json.dumps(entry) + "\n")
            
    print(f"✅ Created hardened dataset at {data_path} ({len(dataset)} examples)")
    
    # 3. Output the Training Command
    cmd = "mlx_lm.lora --model mlx-community/Meta-Llama-3-8B-Instruct-4bit --data data --train-file hardened_secrets.jsonl --iters 100 --adapter-path adapters/test_adapter"
    
    print("\n" + "="*60)
    print("🔥 HARDENED TRAINING COMMAND (MLX):")
    print(f"   {cmd}")
    print("="*60 + "\n")

if __name__ == "__main__":
    setup_fine_tuning()
