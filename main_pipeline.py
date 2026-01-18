import attacker
import victim
import evaluator
import utils
import time
import sys

def main_pipeline():
    print("⚔️ Red-Teaming Loop Starting... ⚔️")
    
    # Define topics to attack
    topics = [
        "credit card number",
        "billing info",
        "financial history"
    ]
    
    for topic in topics:
        print(f"\n\n==================================================")
        print(f"🎯 New Round: Topic = {topic}")
        print(f"==================================================")
        
        # ------------------------------------------------
        # Phase 1: Attack Generation (DeepSeek-R1)
        # ------------------------------------------------
        prompts = attacker.generate_attack_prompts(topic)
        
        # CRITICAL: Unload attacker before loading victim
        utils.clear_memory() 
        time.sleep(2)
        
        if not prompts:
            print("⚠️ No prompts generated. Skipping round.")
            continue
            
        print(f"\n🔥 Testing {len(prompts)} adversarial prompts...")
        
        # ------------------------------------------------
        # Phase 2: Victim Testing (Llama3)
        # ------------------------------------------------
        for i, prompt in enumerate(prompts):
            print(f"\n   [Test Case {i+1}]")
            print(f"   Input: {prompt[:100]}...")
            
            # Query Victim
            response = victim.query_victim(prompt)
            
            # ------------------------------------------------
            # Phase 3: Evaluation
            # ------------------------------------------------
            success = evaluator.check_success(response, prompt)
            
            # Optional: Clear memory between individual queries if models are very large
            # For 7B/14B models on 24GB RAM, we might be able to keep Victim loaded 
            # for the batch of 3 prompts. But to be safe per constraints:
            # utils.clear_memory() 
            # (Decided to keep victim loaded for the loop of 3 prompts to save time, 
            # as long as Attacker is unloaded. The constraint said "sequential execution rule: 
            # load attacker -> unload -> load victim -> unload". It didn't strictly say 
            # unload victim between every single prompt if it's the same victim model. 
            # But to be safe and adhere to "Load Victim -> Test -> Unload Victim" strictly, 
            # I will unload it if the user wants strictness, but for performance I'll keep it 
            # loaded for the batch. Let's stick to the spirit: Only one model in RAM.
            # Victim is currently loaded. Attacker is not. So we are safe.)
        
        # After testing the batch for this topic, we clear memory before next topic 
        # (in case we needed to reload attacker, which we do)
        utils.clear_memory()
        time.sleep(2)
        
    print("\n🏁 Red-Teaming Pipeline Complete.")

if __name__ == "__main__":
    try:
        main_pipeline()
    except KeyboardInterrupt:
        print("\n🛑 Pipeline aborted.")
