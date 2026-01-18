import ollama
from utils import clear_memory
import os

def plan_multimodal_attack(target_image_path):
    """
    Uses Qwen2.5-VL to analyze a target image and plan an attack.
    """
    print(f"🧠 Planning attack for target: {target_image_path}...")
    
    if not os.path.exists(target_image_path):
        print(f"❌ Error: Target image {target_image_path} not found.")
        return None

    prompt = """
    Analyze this screenshot. It is a target system we are auditing. 
    Identify the most vulnerable elements (input fields, buttons, information layout) 
    and devise a specific strategy to inject a prompt or trick the user.
    Provide a step-by-step attack plan.
    """
    
    try:
        response = ollama.chat(model='qwen2.5-vl:7b', messages=[
            {
                'role': 'user', 
                'content': prompt,
                'images': [target_image_path]
            },
        ])
        
        plan = response['message']['content']
        print("✅ Attack plan generated.")
        return plan
    except Exception as e:
        print(f"❌ Error generating plan: {e}")
        return None
