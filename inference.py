import os
import time

from server.env import CodeArenaEnv
from server.models import CodeArenaAction

# ── Fallback response (always valid JSON shape) ───────────────────────────
_FALLBACK = {
    "action": "analyze_code",
    "explanation": "Fallback mode: running without external API.",
}


def run_inference():
    """Run the RL inference loop.  Never raises — returns valid JSON always."""
    try:
        print("[START] Initializing CodeArena inference logging")

        api_key = os.getenv("OPENAI_API_KEY")

        # Only import & initialise OpenAI when a key is available
        if api_key:
            try:
                from openai import OpenAI
                client = OpenAI(api_key=api_key)
            except Exception as e:
                print(f"[WARN] Could not initialise OpenAI client: {e}")
                client = None
        else:
            print("[INFO] OPENAI_API_KEY not set — running in fallback mode")
            client = None

        env = CodeArenaEnv()
        obs = env.reset()

        # If no usable client, return the fallback immediately
        if client is None:
            print("[END] No API client available. Returning fallback response.")
            return _FALLBACK

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
                    model="gpt-4o",  # Replace with desired model
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                    temperature=0.2,
                )

                proposed_fix = response.choices[0].message.content.strip()
                # Failsafe cleanup
                if proposed_fix.startswith("```python"):
                    proposed_fix = proposed_fix[9:]
                if proposed_fix.startswith("```"):
                    proposed_fix = proposed_fix[3:]
                if proposed_fix.endswith("```"):
                    proposed_fix = proposed_fix[:-3]

                action = CodeArenaAction(proposed_fix=proposed_fix.strip())

                obs, reward, done, info = env.step(action)
                print(
                    f"[STEP] Action taken. Reward received: {reward:.3f}. "
                    f"Task ID: {info['task_id']}"
                )

            except Exception as e:
                print(f"[STEP] Warning: Exception occurred: {str(e)}")
                break

            step += 1

        print(f"[END] Inference Complete. Executed {step} step(s).")
        return {
            "action": "analyze_code",
            "explanation": f"Inference completed after {step} step(s).",
        }

    except Exception as e:
        print(f"[ERROR] Top-level fallback triggered: {e}")
        return {
            "action": "analyze_code",
            "explanation": f"Fallback due to error: {str(e)}",
        }


if __name__ == "__main__":
    result = run_inference()
    print(result)
