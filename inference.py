import os
import time
from openai import OpenAI
from server.env import CodeArenaEnv
from server.models import CodeArenaAction

def run_inference():
    print("[START] Initializing CodeArena inference logging")
    
    client = OpenAI(
        # Uses OPENAI_API_KEY from environment by default
        # You can substitute this with any compatible endpoint
    )
    env = CodeArenaEnv()
    obs = env.reset()
    
    system_prompt = """You are an expert autonomous code repair agent.
Your goal is to fix the buggy code provided to you.
Ensure your code is highly efficient and fully resolves all logical, syntax, and algorithmic bugs.
Only return the fixed raw Python code. Do not output markdown blocks (like ```python). Do not explain your changes."""

    done = False
    step = 0
    
    while not done and step < env.max_steps:
        print(f"[STEP] Beginning Step {step + 1}")
        
        user_prompt = f"""
Buggy Code:
{obs.buggy_code}

Error Log:
{obs.error_log}

Test Results:
{obs.test_results}
"""
        try:
            response = client.chat.completions.create(
                model="gpt-4o", # Replace with desired model
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.2
            )
            
            proposed_fix = response.choices[0].message.content.strip()
            # Failsafe cleanup
            if proposed_fix.startswith("```python"): proposed_fix = proposed_fix[9:]
            if proposed_fix.startswith("```"): proposed_fix = proposed_fix[3:]
            if proposed_fix.endswith("```"): proposed_fix = proposed_fix[:-3]
                
            action = CodeArenaAction(proposed_fix=proposed_fix.strip())
            
            obs, reward, done, info = env.step(action)
            print(f"[STEP] Action taken. Reward received: {reward:.3f}. Task ID: {info['task_id']}")
            
        except Exception as e:
            print(f"[STEP] Warning: Exception occurred: {str(e)}")
            break
            
        step += 1
        
    print(f"[END] Inference Complete. Executed {step} step(s).")

if __name__ == "__main__":
    run_inference()
