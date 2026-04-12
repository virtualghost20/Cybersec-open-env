import sys
import os

# Allow importing app from root
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app import reset_env, step_env


def test_reset_returns_valid_state():
    state = reset_env()
    assert isinstance(state, dict), "State must be a dict"
    assert "vulnerabilities" in state
    assert "risk_level" in state
    assert "system_status" in state
    assert 3 <= state["vulnerabilities"] <= 5
    assert 0.0 <= state["risk_level"] <= 1.0
    assert isinstance(state["system_status"], str)


def test_step_scan():
    reset_env()
    next_state, reward, done, info = step_env("scan")
    assert isinstance(next_state, dict)
    assert 0.0 <= reward <= 1.0
    assert isinstance(done, bool)
    assert isinstance(info, dict)


def test_step_exploit():
    reset_env()
    next_state, reward, done, info = step_env("exploit")
    assert 0.0 <= reward <= 1.0


def test_step_defend():
    reset_env()
    next_state, reward, done, info = step_env("defend")
    assert 0.0 <= reward <= 1.0
    # risk_level should decrease after defend
    initial_state = reset_env()
    initial_risk = initial_state["risk_level"]
    next_state2, _, _, _ = step_env("defend")
    # risk should go down (or stay at 0)
    assert next_state2["risk_level"] <= initial_risk


def test_termination_on_max_steps():
    reset_env()
    done = False
    for _ in range(20):
        _, _, done, _ = step_env("scan")
        if done:
            break
    assert done, "Environment should terminate within max steps"


def test_reward_always_in_range():
    reset_env()
    for action in ["scan", "exploit", "defend", "scan", "defend"]:
        _, reward, done, _ = step_env(action)
        assert 0.0 <= reward <= 1.0, f"Reward {reward} out of range for action {action}"
        if done:
            break

