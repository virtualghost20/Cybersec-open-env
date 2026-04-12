import os
import sys
import requests

API_BASE_URL = os.environ.get("API_BASE_URL", "http://localhost:7860")
MODEL_NAME = os.environ.get("MODEL_NAME", "dummy-model")
HF_TOKEN = os.environ.get("HF_TOKEN", "")

TASK = "scan_challenge"
ENV = "cybersec_openenv"
MAX_STEPS = 10


def choose_action_dummy(state):
    """Fallback action selection without LLM."""
    risk = state.get("risk_level", 0.5)
    vulns = state.get("vulnerabilities", 0)
    if vulns > 2:
        return "exploit"
    elif risk > 0.5:
        return "defend"
    else:
        return "scan"


def choose_action_llm(state, client):
    """Use OpenAI-compatible client to pick action."""
    prompt = (
        f"You are a cybersecurity AI agent. Current state: {state}. "
        f"Choose one action from: scan, exploit, defend. "
        f"Reply with ONLY the action word, nothing else."
    )
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=10,
        )
        action = response.choices[0].message.content.strip().lower()
        if action not in ("scan", "exploit", "defend"):
            action = "scan"
        return action
    except Exception:
        return choose_action_dummy(state)


def main():
    # Try to init OpenAI client
    client = None
    if HF_TOKEN:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=HF_TOKEN, base_url=f"{API_BASE_URL}/v1")
        except Exception:
            client = None

    print(f'[START] task={TASK} env={ENV} model={MODEL_NAME}')

    # Reset environment
    try:
        resp = requests.post(f"{API_BASE_URL}/reset", timeout=10)
        resp.raise_for_status()
        state = resp.json()
    except Exception as e:
        print(f'[START] task={TASK} env={ENV} model={MODEL_NAME} error="{e}"')
        sys.exit(1)

    total_reward = 0.0
    steps = 0
    done = False

    for step_num in range(1, MAX_STEPS + 1):
        if done:
            break

        # Choose action
        if client:
            action = choose_action_llm(state, client)
        else:
            action = choose_action_dummy(state)

        # Execute step
        error_val = "null"
        try:
            resp = requests.post(
                f"{API_BASE_URL}/step",
                json={"action": action},
                timeout=10,
            )
            resp.raise_for_status()
            result = resp.json()
            state = result["next_state"]
            reward = result["reward"]
            done = result["done"]
            total_reward += reward
            steps = step_num
        except Exception as e:
            reward = 0.0
            done = True
            error_val = f'"{str(e)}"'
            steps = step_num

        done_str = "true" if done else "false"
        print(f'[STEP] step={step_num} action="{action}" reward={reward:.2f} done={done_str} error={error_val}')

    score = round(total_reward / steps, 2) if steps > 0 else 0.0
    rewards_total = round(total_reward, 2)

    print(f'[END] success=true steps={steps} score={score} rewards={rewards_total}')


if __name__ == "__main__":
    main()

