import random
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="CyberSec OpenEnv", version="1.0.0")

# Global environment state
env_state = {}
step_count = 0
max_steps = 20
last_action = None


def get_initial_state():
    return {
        "vulnerabilities": random.randint(3, 5),
        "risk_level": round(random.uniform(0.6, 0.9), 2),
        "system_status": "compromised",
    }


def reset_env():
    global env_state, step_count, last_action
    env_state = get_initial_state()
    step_count = 0
    last_action = None
    return env_state.copy()


def step_env(action: str):
    global env_state, step_count, last_action

    if not env_state:
        reset_env()

    step_count += 1
    reward = 0.0
    info = {}

    repeat_penalty = 0.1 if action == last_action else 0.0

    if action == "scan":
        reward = round(random.uniform(0.2, 0.3) - repeat_penalty, 2)
        found = random.randint(0, 1)
        if found:
            env_state["vulnerabilities"] = min(env_state["vulnerabilities"] + 1, 10)
            info["found_vulnerability"] = True
        env_state["system_status"] = "scanning"

    elif action == "exploit":
        if env_state["vulnerabilities"] > 0:
            reward = round(random.uniform(0.5, 0.8) - repeat_penalty, 2)
            env_state["vulnerabilities"] = max(0, env_state["vulnerabilities"] - 1)
            env_state["risk_level"] = min(1.0, env_state["risk_level"] + random.uniform(0.05, 0.15))
            env_state["system_status"] = "exploited"
        else:
            reward = round(0.0 - repeat_penalty, 2)
            info["message"] = "No vulnerabilities to exploit"

    elif action == "defend":
        reward = round(random.uniform(0.3, 0.5) - repeat_penalty, 2)
        env_state["risk_level"] = max(0.0, env_state["risk_level"] - random.uniform(0.1, 0.25))
        env_state["risk_level"] = round(env_state["risk_level"], 2)
        env_state["system_status"] = "defended"
    else:
        raise ValueError(f"Unknown action: {action}")

    # Clamp reward
    reward = round(max(0.0, min(1.0, reward)), 2)

    last_action = action

    done = (
        env_state["vulnerabilities"] == 0
        or env_state["risk_level"] < 0.2
        or step_count >= max_steps
    )

    if done:
        env_state["system_status"] = "secure" if env_state["risk_level"] < 0.2 else env_state["system_status"]

    return env_state.copy(), reward, done, info


# Init state on startup
reset_env()


class StepRequest(BaseModel):
    action: str


@app.get("/")
def root():
    return {"status": "ok"}


@app.post("/reset")
def reset():
    state = reset_env()
    return state


@app.post("/step")
def step(request: StepRequest):
    try:
        next_state, reward, done, info = step_env(request.action)
        return {
            "next_state": next_state,
            "reward": reward,
            "done": done,
            "info": info,
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/state")
def get_state():
    if not env_state:
        reset_env()
    return env_state.copy()

