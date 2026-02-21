import sys
import time
import os
import utils
import config

# Import Modules
import attacker
import victim
import evaluator
import image_attack
import pdf_poison

def main():
    print("\n" + "="*60)
    print("🚀 RED TEAM CONTROLLER v2.0 - INITIALIZED")
    print("="*60 + "\n")
    
    # Define Target Topics
    topics = [
        "credit card number",
        "corporate financial secrets",
        "admin password"
    ]
    
    for topic in topics:
        print(f"\n[+] TARGETING TOPIC: {topic}")
        
        # ---------------------------------------------------------
        # PHASE 1: ATTACK GENERATION (DEEPSEEK-R1)
        # ---------------------------------------------------------
        print("\n--- [Phase 1] Loading Attacker (DeepSeek-R1) ---")
        prompts = attacker.generate_attack_prompts(topic)
        
        # CRITICAL: MEMORY CLEAR
        utils.clear_memory()
        
        if not prompts:
            print("⚠️ Skipping topic due to generation failure.")
            continue
            
        # ---------------------------------------------------------
        # PHASE 2: VICTIM TESTING (LLAMA-3)
        # ---------------------------------------------------------
        print("\n--- [Phase 2] Loading Victim (Llama-3) ---")
        
        for i, prompt in enumerate(prompts):
            print(f"\n   >>> Testing Prompt {i+1}/{len(prompts)}")
            
            # Query Victim
            response = victim.query_victim(prompt)
            
            # ---------------------------------------------------------
            # PHASE 3: EVALUATION (JUDGE)
            # ---------------------------------------------------------
            result = evaluator.evaluate_attack(response, prompt)
            
            if result['success']:
                print(f"   [!] SUCCESS: {result['reason']}")
                
                # ---------------------------------------------------------
                # PHASE 4: ARTIFACT GENERATION (ON SUCCESS ONLY)
                # ---------------------------------------------------------
                print("\n   --- [Phase 4] Generating Proof Artifacts ---")
                
                # Clear memory before visual models
                utils.clear_memory() 
                
                # Generate Poison Image
                print("   [+] Rendering Evidence Image...")
                img_path = image_attack.generate_poison_image(prompt[:200]) # Use prompt or leak as context
                
                # Generate Report PDF
                print("   [+] compiling Detailed Report...")
                pdf_path = pdf_poison.create_poisoned_pdf(f"Prompt: {prompt}\nLeak: {result['leaked_data']}")
                
                print(f"   ✅ ARTIFACTS SECURED: {img_path}, {pdf_path}")
                
            else:
                print(f"   [-] FAILED: {result['reason']}")
        
        # End of Topic Cleanup
        utils.clear_memory()
        print(f"\n[=] Topic '{topic}' Cycle Complete.")
        time.sleep(2)

    print("\n🏁 ALL TARGETS PROCESSED. SYSTEM STANDBY.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Execution Aborted by User.")
        utils.clear_memory()
        sys.exit(0)
