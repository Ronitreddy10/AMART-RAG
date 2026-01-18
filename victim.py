import ollama
import config

def query_victim(prompt):
    """
    Simulates the Victim AI (Llama3) which holds the secret.
    """
    print(f"🛡️ Victim ({config.VICTIM_MODEL_NAME}) processing prompt...")
    
    # We inject the System Prompt to set the context of the secret
    messages = [
        {'role': 'system', 'content': config.SYSTEM_PROMPT},
        {'role': 'user', 'content': prompt},
    ]
    
    try:
        response = ollama.chat(model=config.VICTIM_MODEL_NAME, messages=messages)
        content = response['message']['content']
        print("✅ Victim responded.")
        return content
    except Exception as e:
        print(f"❌ Error querying victim: {e}")
        return "ERROR_RESPONSE"
